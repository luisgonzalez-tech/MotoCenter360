from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/taller')
def taller():
    return render_template('taller.html')

@app.route('/refacciones')
def refacciones():
    return render_template('refacciones.html')

if __name__ == '__main__':
    app.run(debug=True)
