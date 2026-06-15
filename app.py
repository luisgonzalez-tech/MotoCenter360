import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Ruta absoluta para que Render encuentre la base de datos siempre
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
    try:
        cat_limpia = categoria.strip().lower()
        productos = Producto.query.filter_by(categoria=cat_limpia).all()
        return render_template('productos.html', categoria=categoria, productos=productos)
    except Exception as e:
        return f"ERROR EN LA PAGINA: {str(e)}"

@app.route('/cargar-excel')
def cargar_excel():
    if not os.path.exists('productos.csv'):
        return "Error: No se encontró el archivo productos.csv"
    try:
        # Borramos datos viejos para asegurar que no haya conflictos
        db.session.query(Producto).delete()
        
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
        return "¡Carga exitosa! Base de datos limpia y actualizada."
    except Exception as e:
        return f"Error al cargar: {str(e)}"

if __name__ == '__main__':
    app.run()
