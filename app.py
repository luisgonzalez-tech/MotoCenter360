from flask import Flask, render_template
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
