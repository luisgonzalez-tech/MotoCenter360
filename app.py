from flask import Flask, render_template

app = Flask(__name__)

inventario = {
    "Aceite": 15,
    "Balatas": 10,
    "Filtros": 8
}

@app.route('/')
def index():
    return render_template('index.html', stock=inventario)