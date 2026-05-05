# Importamos la clase Flask desde el paquete instalado
from flask import Flask, render_template
import sqlite3  

# Creamos una instancia de la aplicación. __name__ ayuda a Flask a localizar archivos
app = Flask(__name__)

# Definimos una ruta. El símbolo @ es un decorador que vincula la URL con la función de abajo
@app.route("/")
def ver_coleccion():
    # 1. Conectamos con el archivo de la base de datos
    conexion = sqlite3.connect("peliculas_gestor.db")
    
    # 2. Configuramos la conexión para que devuelva diccionarios (más fácil para Jinja2)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    # 3. Ejecutamos la consulta SQL
    cursor.execute("SELECT * FROM peliculas")

    # 4. Guardamos todos los resultados en una variable
    datos = cursor.fetchall()
    # Convertimos cada fila sqlite3.Row a dict para un uso más sencillo en Jinja
    datos = [dict(row) for row in datos]
    
    # 5. Cerramos la conexión
    conexion.close()













    
    
    # 6. Enviamos los datos reales (como dicts) a la plantilla
    return render_template("index.html", items=datos)

# Comprobamos si el script se está ejecutando directamente (y no importado como módulo)
if __name__ == "__main__":
    # Arrancamos el servidor en modo debug para que se reinicie solo al guardar cambios
    app.run(debug=True)
