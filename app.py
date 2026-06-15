from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motocenter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Base de Datos basado exactamente en tu Excel
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False) # aceites, bujias, etc.
    nombre = db.Column(db.String(200), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

# ==========================================
# 1. RUTA DE INICIO (¡Aquí se conserva tu diseño intacto!)
# ==========================================
@app.route('/')
def inicio():
    return render_template('index.html')

# ==========================================
# 2. SECCIÓN DE REFACCIONES (Los 5 Botones)
# ==========================================
@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

# ==========================================
# 3. VISTA DE PRODUCTOS (Filtros + Catálogo)
# ==========================================
@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    # Filtra los productos de la base de datos según la categoría de la URL
    productos_filtrados = Producto.query.filter_by(categoria=categoria).all()
    return render_template('productos.html', categoria=categoria, productos=productos_filtrados)

if __name__ == '__main__':
    # Esto asegura que la base de datos se cree en Render automáticamente
    with app.app_context():
        db.create_all()
    app.run(debug=True)
