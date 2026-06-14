from flask import Flask, render_template

app = Flask(__name__)

# Definimos la lista aquí para asegurar que siempre esté disponible
CATEGORIAS = [
    "Aceites", "Amortiguadores", "Asientos", "Baterías", "Bujías", 
    "Cables", "Cámaras", "Carrocería/Plásticos", "Cascos", "Embragues", 
    "Escape/Silenciador", "Espejos", "Filtros", "Frenos", "Herramientas", 
    "Llantas", "Luces", "Manubrios y Mandos", "Motores y sus Partes", 
    "Parches", "Parrillas y Defensas", "Posapies/Paradores", "Productos Químicos", 
    "Puños", "Rines, Aros, Ruedas", "Ruedas", "Sistema Combustible", 
    "Sistema Eléctrico", "Sistema Enfriamiento", "Sistema Transmisión", 
    "Soportes", "Velocímetros"
]

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html', categorias=CATEGORIAS)

# ... (tus otras rutas: @app.route('/'), @app.route('/taller'), etc.)
