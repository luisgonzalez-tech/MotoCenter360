@app.route('/refacciones/<categoria>')
def categoria_productos(categoria):
    # Convertimos la categoría recibida en la URL a minúsculas
    cat_buscada = categoria.strip().lower()
    # Buscamos en la base de datos comparando siempre con minúsculas
    productos = Producto.query.filter_by(categoria=cat_buscada).all()
    
    # Pasamos los productos encontrados a tu template
    return render_template('productos.html', categoria=categoria, productos=productos)

@app.route('/cargar-excel')
def cargar_excel():
    try:
        # Borramos todo para evitar duplicados o errores previos
        db.session.query(Producto).delete()
        with open('productos.csv', newline='', encoding='latin-1') as f:
            for fila in csv.DictReader(f):
                # Guardamos la categoría SIEMPRE en minúsculas
                db.session.add(Producto(
                    categoria=fila['categoria'].strip().lower(),
                    nombre=fila['nombre'].strip(),
                    marca=fila['marca'].strip(),
                    precio=float(fila['precio']),
                    imagen_url=fila['imagen_url'].strip()
                ))
        db.session.commit()
        return "Carga exitosa y normalizada."
    except Exception as e:
        return f"Error: {e}"
