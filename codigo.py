
# --- Importamos Tkinter para la interfaz y sqlite3 para la base de datos ---
import tkinter as tk
import sqlite3

# --- Nombre de la base de datos (database) ---
DB_NAME = 'peliculas_gestor.db'

# --- Función que establece la conexión con la base de datos  ---
def conectar_db():
    conexion = sqlite3.connect(DB_NAME) # --- Abrir o crear base de datos ---
    cursor = conexion.cursor() # --- Crear cursor para ejecutar SQL ---
    return conexion, cursor

# --- Función que crea la tabla de películas ---
def inicializar_db():
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

# --- Creación de clase para representar una película con todos sus datos ---
class Pelicula:
    def __init__(self, nombre, descripcion, director, protagonista, valoracion, prioridad="Alta", completada=False):
        self.id = None  # --- Lo asigna la base de datos ---
        self.nombre = nombre
        self.descripcion = descripcion
        self.director = director
        self.protagonista = protagonista
        self.valoracion = valoracion
        self.prioridad = prioridad
        self.completada = completada

# --- Muestra los campos de texto de la película en pantalla (con FUNCIÓN STR, que "imprime") ---
    def __str__(self):
        return (f"{self.nombre} | {self.descripcion} | {self.director} | "
                f"{self.protagonista} | {self.valoracion} | {self.prioridad}")


# --- Interfaz gráfica TKINTER ---

# --- Ventana Principal ---
ventana = tk.Tk()
ventana.title("Gestor de películas")
ventana.geometry("700x700")
ventana.configure(bg="#2E3440")

# --- Para centrar el frame ---
frame_centrado = tk.Frame(ventana, bg="#2E3440")
frame_centrado.place(relx=0.5, rely=0.5, anchor="center")

# --- Frame de los campos de texto ---
frame_formulario = tk.Frame(frame_centrado, bg="#2E3440")
frame_formulario.grid(row=0, column=0, padx=10, pady=10)

# --- Diccionario para los nombres de cada campo ---
campos_info = {
    "Nombre": {},
    "Descripción": {},
    "Director": {},
    "Protagonista": {},
    "Valoración": {},
    "Prioridad": {}
}

# --- Crear etiquetas y campos dinámicamente ---
# PABLO
# BUCLE PARA CREAR LAS ETIQUETAS Y CAJAS DE TEXTO
for idx, etiqueta in enumerate(campos_info.keys()):  # enumerate da el índice (idx) y la clave (etiqueta). keys() = nombres de los campos
    lbl = tk.Label(                                   # Creamos una etiqueta de texto (Label)
        frame_formulario,                             # frame_formulario = contenedor donde se coloca la etiqueta
        text=f"{etiqueta}:",                          # El texto que se muestra
        fg="black",                                   # fg = black = color del texto
        bg="#D3D3D3",                                 # bg = D3D3D3 = color del fondo de la etiqueta
        font=("Arial", 12))                           # Tipo de letra y tamaño

    entry = tk.Entry(frame_formulario, width=50)      # Caja de texto donde el usuario escribirá (Entry), width=ancho
# lbl.grid es un método que coloca la etiqueta en una tabla
    lbl.grid(row=idx, column=2, padx=5, pady=5, ipady=5)   # Colocamos la etiqueta en la fila "idx" y columna 2
                                                            # padx/pady = separación y espacio alrededor, ipady = aumenta el espacio

    entry.grid(row=idx, column=3, padx=5, pady=5, ipady=5) # Colocamos la caja de texto en la tabla, justo en la columna 3 junto a su etiqueta

    campos_info[etiqueta]["entry"] = entry            # Guardamos la caja de texto dentro del "diccionario" para usarla después


# ---------------- LISTA DE TAREAS ----------------

frame_lista = tk.Frame(frame_centrado)               # Creamos un frame (contenedor) para meter la lista y su scrollbar
frame_lista.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")  # Lo colocamos usando grid. sticky="nsew" = se estira en todas las direcciones

lista_tareas = tk.Listbox(frame_lista, width=100, height=10)   # Listbox = lista donde se mostrarán elementos
scrollbar = tk.Scrollbar(frame_lista, orient="vertical",        # Scrollbar = barra de desplazamiento vertical
                         command=lista_tareas.yview)            # Indica que al mover la scrollbar debe cambiar la vista vertical de la lista
lista_tareas.config(yscrollcommand=scrollbar.set)               # Conectamos la lista con la scrollbar para que funcionen juntos

lista_tareas.grid(row=0, column=2, sticky="nsew")               # Colocamos la lista en la columna 2
scrollbar.grid(row=0, column=3, sticky="ns")                    # Colocamos la barra en la columna 3, de arriba a abajo (ns = norte/sur)

frame_lista.grid_rowconfigure(0, weight=1)                      # Permite que la fila 0 se expanda con la ventana
frame_lista.grid_columnconfigure(0, weight=1)                   # Permite que la columna 0 se expanda


# ---------------- BARRA DE ESTADO ----------------

barra_estado = tk.Label(
    frame_centrado,                   # Contenedor donde va la barra de estado
    text="Listo",                     # Texto que se mostrará
    fg="black",                       # Color del texto
    bg="#81A1C1",                     # Color del fondo
    font=("Arial", 12))               # Fuente y tamaño

barra_estado.grid(row=3, column=0, padx=10, pady=10, sticky="ew")  # Colocamos la barra de estado abajo. sticky="ew" = se estira horizontalmente (este-oeste)


# ALVARO
# --- Funciones de los botones ---

def añadir_pelicula():
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


# PABLO
# --- Frame: Botones ---
# Contenedor donde van los botones (color de fondo (bg))
frame_botones = tk.Frame(frame_centrado, bg="#88C0D0")

# Colocamos el contenedor en la tabla
frame_botones.grid(row=2, column=0, padx=10, pady=10)

# Lista con el texto del botón y la función que los ejecuta
botones = [
    ("Añadir Película", añadir_pelicula),
    ("Modificar Película", modificar_pelicula),
    ("Eliminar Película", eliminar_pelicula)
]

# Creamos cada botón dentro del frame, el comando es la función que se ejecuta cuando pulsas el botón
for i, (texto, comando) in enumerate(botones):
    btn = tk.Button(
        frame_botones, text=texto, fg="black", bg="#88C0D0",
        font=("Arial", 12), command=comando # command=comando:es la función que se ejecuta al pulsar el botón
    )
    
  # Colocamos cada botón en la misma fila pero en columnas diferentes
    btn.grid(row=0, column=i, padx=10, pady=5)

# Vinculamos la lista_tareas a una acción
lista_tareas.bind('<<ListboxSelect>>', cargar_seleccion) # ListboxSelect ocurre cuando se selecciona un elemento y cuando se selecciona una película ocurre: cargar_seleccion

# --- Cargar inicial desde BD ---

# ALEX

# --- Función que carga las películas de la base de datos y las muestra en la lista de películas ---
def cargar_peliculas_iniciales():
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

# --- Ejecución principal ---
if __name__ == "__main__":
    inicializar_db() # --- Gestiona la base de datos y crea la tabla si no existe ---
    cargar_peliculas_iniciales() # --- Carga las películas en la lista ---
    ventana.mainloop() # --- Muestra la ventana de la App ---
