from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

# CREAR BASE DE DATOS
def init_db():

    conn = sqlite3.connect('empleados.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado TEXT,
            entrada TEXT,
            salida TEXT,
            total TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# PAGINA PRINCIPAL
@app.route('/')
def index():

    conn = sqlite3.connect('empleados.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM registros ORDER BY id DESC')

    registros = cursor.fetchall()

    conn.close()

    return render_template('index.html', registros=registros)

# REGISTRAR ENTRADA
@app.route('/entrada', methods=['POST'])
def entrada():

    empleado = request.form['empleado']

    hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('empleados.db')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO registros (empleado, entrada)
        VALUES (?, ?)
    ''', (empleado, hora_entrada))

    conn.commit()
    conn.close()

    return redirect('/')

# REGISTRAR SALIDA
@app.route('/salida/<int:id>')
def salida(id):

    conn = sqlite3.connect('empleados.db')

    cursor = conn.cursor()

    cursor.execute('SELECT entrada FROM registros WHERE id = ?', (id,))

    resultado = cursor.fetchone()

    if resultado:

        entrada_str = resultado[0]

        entrada = datetime.strptime(
            entrada_str,
            '%Y-%m-%d %H:%M:%S'
        )

        hora_salida = datetime.now()

        diferencia = hora_salida - entrada

        total_segundos = int(diferencia.total_seconds())

        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60

        tiempo_total = f'{horas:02}:{minutos:02}:{segundos:02}'

        cursor.execute('''
            UPDATE registros
            SET salida = ?, total = ?
            WHERE id = ?
        ''', (
            hora_salida.strftime('%Y-%m-%d %H:%M:%S'),
            tiempo_total,
            id
        ))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')