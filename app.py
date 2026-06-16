import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'motocenter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

# --- AUTO-CARGA DE DATOS ---
with app.app_context():
    db.create_all()
    # Si la base de datos está vacía, cargamos el CSV automáticamente
    if Producto.query.count() == 0:
        try:
            with open('productos.csv', mode='r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    db.session.add(Producto(
                        categoria=fila['categoria'].strip().lower(),
                        nombre=fila['nombre'].strip(),
                        marca=fila['marca'].strip(),
                        precio=float(fila['precio']),
                        imagen_url=fila['imagen_url'].strip()
                    ))
                db.session.commit()
                print("CSV cargado automáticamente al iniciar.")
        except Exception as e:
            print(f"Error al cargar CSV: {e}")

# --- RUTAS ---
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    cat_buscada = categoria.strip().lower()
    productos = Producto.query.filter(Producto.categoria.ilike(f"%{cat_buscada}%")).all()
    return render_template('productos.html', categoria=categoria, productos=productos)

@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    return redirect(request.referrer or url_for('refacciones'))

@app.route('/cargar-excel')
def cargar_excel():
    try:
        db.session.query(Producto).delete()
        with open('productos.csv', mode='r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                db.session.add(Producto(
                    categoria=fila['categoria'].strip().lower(),
                    nombre=fila['nombre'].strip(),
                    marca=fila['marca'].strip(),
                    precio=float(fila['precio']),
                    imagen_url=fila['imagen_url'].strip()
                ))
            db.session.commit()
        return "Carga manual exitosa."
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
