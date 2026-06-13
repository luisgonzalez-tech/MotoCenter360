from flask import Flask, render_template

app = Flask(__name__)

# Esta es nuestra "Base de datos" temporal en memoria
inventario = {
    "Aceite": 15,
    "Balatas": 10,
    "Filtros": 8
}

@app.route('/')
def index():
    return render_template('index.html', stock=inventario)

if __name__ == '__main__':
    app.run(debug=True)