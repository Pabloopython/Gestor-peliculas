# Importamos la clase Flask desde el paquete instalado
from flask import Flask

# Creamos una instancia de la aplicación. __name__ ayuda a Flask a localizar archivos
app = Flask(__name__)

# Definimos una ruta. El símbolo @ es un decorador que vincula la URL con la función de abajo
@app.route("/") # Cuando el usuario entre en la dirección raíz (home)
def inicio():
    # Esta función devuelve el código HTML que el navegador mostrará al usuario
    return "<h1>GESTOR PELÍCULAS</h1><p>Bienvenido al repositorio de películas.</p>"

# Comprobamos si el script se está ejecutando directamente (y no importado como módulo)
if __name__ == "__main__":
    # Arrancamos el servidor en modo debug para que se reinicie solo al guardar cambios
    app.run(debug=True)