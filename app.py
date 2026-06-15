import csv
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motocenter.db'
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
    # Limpiamos la entrada para evitar errores de búsqueda
    cat_limpia = categoria.strip().lower()
    # Buscamos los productos
    productos = Producto.query.filter_by(categoria=cat_limpia).all()
    # Enviamos a la plantilla. Si 'productos' está vacío, la plantilla debe saber manejarlo.
    return render_template('productos.html', categoria=categoria, productos=productos)

@app.route('/cargar-excel')
def cargar_excel():
    if not os.path.exists('productos.csv'):
        return "Error: No se encontró productos.csv"
    try:
        with open('productos.csv', newline='', encoding='latin-1') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                p = Producto(
                    categoria=fila['categoria'].strip().lower(),
                    nombre=fila['nombre'].strip(),
                    marca=fila['marca'].strip(),
                    precio=float(fila['precio']),
                    imagen_url=fila['imagen_url'].strip()
                )
                db.session.add(p)
            db.session.commit()
        return "¡Carga exitosa!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
