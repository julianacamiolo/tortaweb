from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'clave_secreta_flask'

# Conección DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tortas'

mysql = MySQL(app)

def ejecutar_consulta(query, parametros=None, metodo='fetchall'):
    cursor = mysql.connection.cursor()
    if parametros:
        cursor.execute(query, parametros)
    else:
        cursor.execute(query)
    if metodo == 'fetchall':
        resultado = cursor.fetchall()
    elif metodo == 'fetchone':
        resultado = cursor.fetchone()
    cursor.close()
    return resultado



@app.route('/')
def index():
    
    tortas = ['Tarta de Ricota', 'Brownie', 'Chesse cake', 'Selva negra']
    pasteles = ['pastel xxl', 'pastel xl', 'pastel mediano', 'pastel pequeño']
    return render_template('index.html', tortas=tortas, pasteles=pasteles)

@app.route('/informacion')
@app.route('/informacion/<string:nombre>')
@app.route('/informacion/<string:nombre>/<apellidos>')
def informacion(nombre=None, apellidos=None):
    texto = ""
    if nombre and apellidos:
        texto = f"Bienvenido, {nombre} {apellidos}"
    return render_template('informacion.html', texto=texto)

@app.route('/pedidos')
@app.route('/pedidos/<redireccion>')
def pedidos(redireccion=None):
    if redireccion:
        return redirect(url_for('pedidos'))
    return render_template('pedidos.html')

@app.route('/cupones', methods=['GET', 'POST'])
def cupones():
    if request.method == 'POST':
        url = request.form['url']
        return redirect(url)
    return render_template('cupones.html')

@app.route('/crear-pedidos', methods=['GET', 'POST'])
def crear_tortas():
    if request.method == 'POST':
        tortas = request.form['tortas']
        pasteles = request.form['pasteles']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tortas (tortas, pasteles, precio, ciudad) VALUES (%s, %s, %s, %s)", (tortas, pasteles, precio, ciudad))
        mysql.connection.commit()
        cursor.close()
        flash('Has comprado el mejor pastel')
        return redirect(url_for('index'))
    return render_template('crear_tortas.html')

@app.route('/tortas')
def tortas():
    tortas = ejecutar_consulta("SELECT * FROM tortas")
    return render_template('tortas.html', tortas=tortas)

@app.route('/borrar-torta/<torta_id>')
def borrar_torta(torta_id):
    ejecutar_consulta("DELETE FROM tortas WHERE id = %s ", (torta_id,))
    flash('La torta ha sido eliminada')
    return redirect(url_for('tortas'))

@app.route('/editar-torta/<int:torta_id>', methods=['GET', 'POST'])
def editar_torta(torta_id):
    if request.method == 'POST':
        tortas = request.form['tortas']
        pasteles = request.form['pasteles']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        ejecutar_consulta("""
            UPDATE tortas
            SET tortas = %s,
                pasteles = %s,
                precio = %s,
                ciudad = %s
            WHERE id =  %s
        """, (tortas, pasteles, precio, ciudad, torta_id), metodo=None)
        flash('Has editado el pedido correctamente')
        return redirect(url_for('tortas'))
    torta = ejecutar_consulta("SELECT * FROM tortas WHERE id = %s", (torta_id,), metodo='fetchone')
    return render_template('crear_tortas.html', torta=torta)



if __name__ == '__main__':
    app.run(debug=True)