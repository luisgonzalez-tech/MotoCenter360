from flask import Flask, render_template

app = Flask(__name__)

# Lista de categorías para que la página de refacciones funcione sin errores
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html', categorias=CATEGORIAS)

@app.route('/taller')
def taller():
    return render_template('taller.html')

if __name__ == '__main__':
    app.run(debug=True)
