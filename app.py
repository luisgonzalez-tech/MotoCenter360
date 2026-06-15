from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motocenter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Base de Datos basado en tu estructura de Excel
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False) # aceites, bujias, amortiguadores, llantas, balatas
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

# ==========================================
# RUTA DE INICIO (Conserva tu diseño intacto)
# ==========================================
@app.route('/')
def inicio():
    return render_template('index.html')

# ==========================================
# SECCIÓN DE REFACCIONES (Menu de 5 botones)
# ==========================================
@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

# ==========================================
# CONTROLADOR DEL CATÁLOGO (Solución al Error 500)
# ==========================================
@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    # Filtra de forma segura los productos por la categoría seleccionada
    productos_filtrados = Producto.query.filter_by(categoria=categoria.lower()).all()
    return render_template('productos.html', categoria=categoria, productos=productos_filtrados)

if __name__ == '__main__':
    # Crea la base de datos automáticamente al arrancar en Render
    with app.app_context():
        db.create_all()
    app.run(debug=True)
