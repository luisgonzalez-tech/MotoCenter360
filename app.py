import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Clave secreta necesaria para que funcione el carrito de compras
app.secret_key = 'motocenter360_secreto_super_seguro'

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

def cargar_datos_csv():
    try:
        if Producto.query.count() == 0:
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
    except Exception as e:
        print(f"Error en auto-carga: {e}")

with app.app_context():
    db.create_all()
    cargar_datos_csv()

# --- RUTAS DE NAVEGACIÓN ---
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    cat_buscada = categoria.strip().lower()
    productos = Producto.query.filter(Producto.categoria.ilike(cat_buscada)).all()
    return render_template('productos.html', categoria=categoria, productos=productos)

# --- NUEVO: BUSCADOR REAL ---
@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').strip()
    if query:
        # Busca si la palabra está en el nombre del producto o en la marca
        productos = Producto.query.filter(
            Producto.nombre.ilike(f'%{query}%') | Producto.marca.ilike(f'%{query}%')
        ).all()
        titulo = f'Resultados para: "{query}"'
    else:
        productos = []
        titulo = 'Búsqueda vacía'
    return render_template('productos.html', categoria=titulo, productos=productos)

# --- NUEVO: LÓGICA DEL CARRITO ---
@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    producto = Producto.query.get_or_404(producto_id)
    
    # Guardamos los datos del producto en la sesión del usuario
    session['carrito'].append({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'imagen_url': producto.imagen_url
    })
    session.modified = True
    
    # Lo mandamos directo a ver su carrito
    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

@app.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('ver_carrito'))

# --- CONTROL DE EXCEL ---
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
        return f"Error al cargar: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
