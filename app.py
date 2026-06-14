from flask import Flask, render_template

app = Flask(__name__)

# Catálogo de categorías (sección refacciones)
# MANTENEMOS la lista para que la página de refacciones funcione
CATEGORIAS_REFACCIONES = [
    "Aceites", "Amortiguadores", "Asientos", "Baterías",
    "Bujías", "Cables", "Cámaras", "Carrocería/Plásticos",
    "Cascos", "Embragues", "Escape/Silenciador", "Espejos",
    "Filtros", "Frenos", "Herramientas", "Llantas",
    "Luces", "Manubrios y Mandos", "Motores y sus Partes", "Parches",
    "Parrillas y Defensas", "Posapies/Paradores", "Productos Químicos", "Puños",
    "Rines, Aros, Ruedas", "Ruedas", "Sistema Combustible", "Sistema Eléctrico",
    "Sistema Enfriamiento", "Sistema Transmisión", "Soportes", "Velocímetros"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/taller')
def taller():
    return render_template('taller.html')

# Agregamos la ruta para refacciones, pasando la lista
@app.route('/refacciones')
def refacciones():
