# En database_manager.py
import sqlite3

DB_NAME = 'database_manager.db'

def conectar_db():
    conexion = sqlite3.connect(DB_NAME) # --- Abrir o crear base de datos ---
    cursor = conexion.cursor() # --- Crear cursor para ejecutar SQL ---
    return conexion, cursor

class database_manager:
        # El constructor ahora solo se encarga de la BD
    def __init__(self, nombre, descripcion, director, protagonista, valoracion, prioridad="Alta", completada=False):
        self.id = None  # --- Lo asigna la base de datos ---
        self.nombre = nombre
        self.descripcion = descripcion
        self.director = director
        self.protagonista = protagonista
        self.valoracion = valoracion
        self.prioridad = prioridad
        self.completada = completada

    def inicializar_db():
        # Este método es idéntico al que ya teníais
        conexion, cursor = conectar_db()
        comando_sql = """
        CREATE TABLE IF NOT EXISTS Peliculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        director TEXT,
        protagonista TEXT,
        valoracion TEXT,
        prioridad TEXT
    )
    """
        cursor.execute(comando_sql) 
        conexion.commit() # --- Guardar los cambios ---
        conexion.close() # --- Cerrar la base de datos ---
        print("Base de datos y tabla 'Peliculas' listas.")

    def añadir_pelicula():
            # Ahora recibe los datos como parámetros
            # En esta parte el código lee todas las entradas que tiene los atributos y revisa si hay alguno que este vacío, además inserta la película en la base de datos y la listbox
            # Obtiene los valores de cada entrada en el mismo orden que los atributos están puestos
        datos = [campos_info[c]["entry"].get().strip() for c in campos_info]
        if not all(datos):
            barra_estado.config(
                text="⚠️ Rellena todos los campos antes de añadir.")
            return  # devuelve ese texto en caso que de que falta algun dato de los atributos
        try:
            # conecta los atributos que le hemos indicado con la base de datos
                conexion, cursor = conectar_db()
                sql = "INSERT INTO Peliculas (nombre, descripcion, director, protagonista, valoracion, prioridad) VALUES (?, ?, ?, ?, ?, ?)"
            # la tupla es como un mini-diccionario en el que están los atributos
                cursor.execute(sql, tuple(datos))
                conexion.commit()
                conexion.close()  # abre y cierra la conexion con la base de datos
            # muestra la pelicula como una linea de texto en la listbox
                pelicula_texto = " | ".join(datos)
                lista_tareas.insert(tk.END, pelicula_texto)
                barra_estado.config(text="✅ Película añadida correctamente.")
                for campo in campos_info.values():
                    campo["entry"].delete(0, tk.END)
        except sqlite3.Error as e:
            # si se produce un error en la base datos devuelve ese texto
                barra_estado.config(text=f"❌ Error de base de datos: {e}")
    
    def actualizar_lista(self):
        # Este método ahora DEVUELVE los datos, no actualiza la GUI
        try:
            conexion, cursor = conectar_db()
            # --- SQL obtiene los datos principales de las películas ---
            sql = "SELECT nombre, descripcion, director, protagonista, valoracion, prioridad FROM Peliculas"
            cursor.execute(sql)
            # ---  Devuelve todas las filas obtenidas de la tabla ---
            registros = cursor.fetchall()
            # ---  Analiza cada película obtenida ---
            for fila in registros:
                pelicula_texto = " | ".join(fila) # --- Convierte los datos de la película en una sola línea de texto ---
                lista_tareas.insert(tk.END, pelicula_texto) # --- Inserta la película dentro de la lista de la interfaz ---
            print(
                f"Se han cargado {len(registros)} películas de la base de datos.")
            # ---  En caso de que ocurra un error al leer la base de datos ---
        except sqlite3.Error as e:
            barra_estado.config(text=f"❌ Error al cargar la base de datos: {e}")
        # ---  Función que se ejecuta siempre para cerrar la conexión  ---
        finally:
            if 'conexion' in locals(): # --- Sólo si existe la variable conexión ---
                conexion.close()

    def modificar_pelicula():
        # nos permite seleccionar la pelicula que queremos modificar
        seleccion = lista_tareas.curselection()
        if not seleccion:
            # si no hemos seleccionado niguna nos devuelve es texto
            barra_estado.config(text="⚠️ Selecciona una película para modificar.")
            return
        index = seleccion[0]  # nos indica que hemos selecionado
        try:
            texto_antiguo = lista_tareas.get(index)
            # cambia los datos que queremos modificar
            nombre_antiguo = texto_antiguo.split(" | ")[0].strip()
        except IndexError:
            barra_estado.config(text="❌ Error al leer la película seleccionada.")
            return

        # introduce los datos nuevos que hemos cambiado antes en la list box
        datos_nuevos = [campos_info[c]["entry"].get().strip() for c in campos_info]
        if not all(datos_nuevos):
            barra_estado.config(
                text="⚠️ Rellena todos los campos antes de modificar.")  # si hay un atributo sin modificar nos devuelve esa frase
            return

        try:
            conexion, cursor = conectar_db()
            sql = """
            UPDATE Peliculas 
            SET nombre=?, descripcion=?, director=?, protagonista=?, valoracion=?, prioridad=?
            WHERE nombre=?      
            """  # actualiza los atributos en la base de datos de SQL
            cursor.execute(sql, tuple(datos_nuevos) + (nombre_antiguo,)
                        )  # ejecuta la tupla con los datos nuevos más el nombre que tiene ahora la película
            conexion.commit()
            conexion.close()
            pelicula_texto_nuevo = " | ".join(datos_nuevos)
            lista_tareas.delete(index)
            lista_tareas.insert(index, pelicula_texto_nuevo)
            barra_estado.config(text="✏️ Película modificada correctamente.")
        except sqlite3.Error as e:
            # las líneas anteriores funcionan igual que en la función de añadir una película (mostrar en la list box, deovlver texto...)
            barra_estado.config(text=f"❌ Error de base de datos: {e}")

    def eliminar_pelicula():
        # eliminamos la pelicula que hemos seleccionado
        seleccion = lista_tareas.curselection()
        if not seleccion:
            barra_estado.config(text="⚠️ Selecciona una película para eliminar.")
            return
        index = seleccion[0]
        try:
            texto_a_borrar = lista_tareas.get(index)
            # elimina la película que hemos eligido de la listbox
            nombre_a_borrar = texto_a_borrar.split(" | ")[0].strip()
        except IndexError:
            barra_estado.config(text="❌ Error al leer la película seleccionada.")
            return
        try:
            conexion, cursor = conectar_db()
            # elimina la película de donde esté guardada en la base de datos
            sql = "DELETE FROM Peliculas WHERE nombre=?"
            cursor.execute(sql, (nombre_a_borrar,))
            conexion.commit()
            conexion.close()
            lista_tareas.delete(index)
            barra_estado.config(text="🗑️ Película eliminada correctamente.")
            for campo in campos_info.values():
                # la pelicula es eliminada completamente de SQL
                campo["entry"].delete(0, tk.END)
        except sqlite3.Error as e:
            barra_estado.config(text=f"❌ Error de base de datos: {e}")

    # --- Función que carga la selección de la Listbox en las entradas ---

    def cargar_seleccion(event=None):
        # sincroniza la listbox con las entradas de los atributos (datos de la película), es decir la película selecciona sale en la entrada de datos
        seleccion = lista_tareas.curselection()
        if not seleccion:
            return  # no hace nada si no pinchamos una película
        index = seleccion[0]
        try:
            # cada atributo de la pelicula que hay en listbos se muestra en su entrada
            texto = lista_tareas.get(index)
            # en la listbox se separa los atributos entre "|"
            partes = [p.strip() for p in texto.split(" | ")]
            keys = list(campos_info.keys())
            # Rellena las entradas una a una con las partes que le corresponde
            # zip(keys, partes) empareja cada clave con su valor correspondiente
            # si hay menos partes que keys, zip truncará al menor de ambos
            # si hay más partes que keys, las partes extra se ignoran
            for k, val in zip(keys, partes):
                entry = campos_info[k]["entry"]
                # elimina si hay algunos datos en la entrada y coloca los nuevos de la pelñicula seleccionada
                entry.delete(0, tk.END)
                entry.insert(0, val)
            barra_estado.config(
                text=f"Seleccionada: {partes[0] if partes else '---'}")  # en la barra de estado nos dice que película hemos seleccionado
        except Exception as e:
            barra_estado.config(text=f"❌ Error al cargar selección: {e}")

    def cargar_peliculas_iniciales():
            conexion, cursor = conectar_db()
            # --- SQL obtiene los datos principales de las películas ---
            sql = "SELECT nombre, descripcion, director, protagonista, valoracion, prioridad FROM Peliculas"
            cursor.execute(sql)
        # ---  Devuelve todas las filas obtenidas de la tabla ---
            registros = cursor.fetchall()
 
            if 'conexion' in locals(): # --- Sólo si existe la variable conexión ---
                conexion.close()
