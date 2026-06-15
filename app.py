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

# IMPORTANTE: Esto asegura que la base de datos se cree en Render automáticamente
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
    # Convertimos a minúsculas para asegurar que coincida con la base de datos
    productos_filtrados = Producto.query.filter_by(categoria=categoria.lower()).all()
    return render_template('productos.html', categoria=categoria, productos=productos_filtrados)

@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    # Por ahora, esta ruta solo recibe el clic y te regresa a la misma página.
    print(f"Producto ID {producto_id} fue agregado al carrito")
    return redirect(request.referrer or '/')

@app.route('/cargar-excel')
def cargar_excel():
    # Esta ruta lee tu CSV y llena la base de datos automáticamente
    if not os.path.exists('productos.csv'):
        return "Error: No se encontró el archivo productos.csv. Asegúrate de haberlo subido a GitHub con ese nombre exacto."
    
    try:
        with open('productos.csv', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            contador = 0
            for fila in lector:
                nuevo_producto = Producto(
                    categoria=fila['categoria'].strip().lower(),
                    nombre=fila['nombre'].strip(),
                    marca=fila['marca'].strip(),
                    precio=float(fila['precio']),
                    imagen_url=fila['imagen_url'].strip()
                )
                db.session.add(nuevo_producto)
                contador += 1
            db.session.commit()
        return f"¡Éxito total! Se cargaron {contador} refacciones a tu base de datos."
    except Exception as e:
        return f"Ocurrió un error al cargar: {e}"

if __name__ == '__main__':
    app.run(debug=True)
