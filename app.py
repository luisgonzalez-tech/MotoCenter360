import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuración de base de datos local
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

# --- AUTO-CARGA AL INICIAR ---
def cargar_datos_csv():
    try:
        if Producto.query.count() == 0:
            with open('productos.csv', mode='r', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    db.session.add(Producto(
                        categoria=fila['categoria'].strip().lower(), # Todo a minúsculas
                        nombre=fila['nombre'].strip(),
                        marca=fila['marca'].strip(),
                        precio=float(fila['precio']),
                        imagen_url=fila['imagen_url'].strip()
                    ))
                db.session.commit()
    except Exception as e:
        print(f"Error en auto-carga: {e}")

with app.app_context():
    db.create_all()
    cargar_datos_csv()

# --- RUTAS ---
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    # .lower() asegura que 'MOTOCICLETA' sea igual a 'motocicleta'
    cat_buscada = categoria.strip().lower()
    productos = Producto.query.filter(Producto.categoria.ilike(cat_buscada)).all()
    return render_template('productos.html', categoria=categoria, productos=productos)

@app.route('/cargar-excel')
def cargar_excel():
    db.session.query(Producto).delete()
    cargar_datos_csv()
    return "Carga manual exitosa."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
