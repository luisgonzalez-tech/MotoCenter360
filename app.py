from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de tu base de datos local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motocenter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tu modelo de inventario (tal como lo tienes en Excel)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False) 
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

# --- RUTA 1: Inicio ---
@app.route('/')
def inicio():
    return render_template('index.html')

# --- RUTA 2: Menú de categorías ---
@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

# --- RUTA 3: La ruta que Render no encontraba (Solución al error) ---
@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    # Esto busca en la base de datos la categoría que el usuario clickeó
    productos_filtrados = Producto.query.filter_by(categoria=categoria).all()
    return render_template('productos.html', categoria=categoria, productos=productos_filtrados)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
