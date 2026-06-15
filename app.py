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
    categoria = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    productos = Producto.query.filter_by(categoria=categoria.strip().lower()).all()
    return render_template('productos.html', categoria=categoria, productos=productos)

# Ruta corregida: Debe coincidir exactamente con el url_for del HTML
@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    print(f"Producto {producto_id} agregado")
    return redirect(request.referrer or url_for('refacciones'))

@app.route('/cargar-excel')
def cargar_excel():
    try:
        db.session.query(Producto).delete()
        with open('productos.csv', newline='', encoding='latin-1') as f:
            for fila in csv.DictReader(f):
                db.session.add(Producto(
                    categoria=fila['categoria'].strip().lower(),
                    nombre=fila['nombre'].strip(),
                    marca=fila['marca'].strip(),
                    precio=float(fila['precio']),
                    imagen_url=fila['imagen_url'].strip()
                ))
        db.session.commit()
        return "Carga exitosa."
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run()
