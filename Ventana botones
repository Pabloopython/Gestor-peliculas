import tkinter as tk
import sqlite3


class Pelicula:

    def __init__(self, nombre, descripcion, director, protagonista, valoracion, prioridad="Alta", completada=False):
        # Creamos los atributos de la película
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.director = director
        self.protagonista = protagonista
        self.valoracion = valoracion
        self.prioridad = prioridad
        self.completada = completada

    def __str__(self):
        return (f"{self.nombre} | {self.descripcion} | {self.director} | "
                f"{self.protagonista} | {self.valoracion} | {self.prioridad}")


# --- Objetos de prueba ---
pelicula1 = Pelicula("Cars", "Infantil/Comedia",
                     "John Lasseter", "Rayo Mcqueen", "5 estrellas", "Alta")
pelicula2 = Pelicula("The Notebook", "Romance",
                     "Nick Cassavetes", "Ryan Gosling", "5 estrellas", "Alta")

print("\n--- DATOS DE LA PELÍCULA 1 ---")
print(pelicula1)
print("\n--- DATOS DE LA PELÍCULA 2 ---")
print(pelicula2)

# --- Ventana Principal ---
ventana = tk.Tk()
ventana.title("Gestor de películas")
ventana.geometry("750x750")
ventana.configure(bg="#2E3440")

# --- Frame: Formulario ---
frame_formulario = tk.Frame(ventana, bg="#2E3440")
frame_formulario.grid(row=0, column=2, padx=10, pady=10)

# --- Diccionario de campos ---
campos_info = {
    "Nombre": {},
    "Descripción": {},
    "Director": {},
    "Protagonista": {},
    "Valoración": {},
    "Prioridad": {},
    "Completado": {}
}

# --- Crear etiquetas y campos dinámicamente ---
for idx, etiqueta in enumerate(campos_info.keys()):
    lbl = tk.Label(
        frame_formulario, text=f"{etiqueta}:", fg="black", bg="#D3D3D3", font=("Arial", 12))
    entry = tk.Entry(frame_formulario, width=50)
    lbl.grid(row=idx, column=1, padx=5, pady=5, ipady=5)
    entry.grid(row=idx, column=2, padx=5, pady=5, ipady=5)
    campos_info[etiqueta]["entry"] = entry

# --- Lista de tareas ---
frame_lista = tk.Frame(ventana)
frame_lista.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

lista_tareas = tk.Listbox(frame_lista, width=100, height=10)
scrollbar = tk.Scrollbar(frame_lista, orient="vertical",
                         command=lista_tareas.yview)
lista_tareas.config(yscrollcommand=scrollbar.set)

lista_tareas.grid(row=0, column=0,)
scrollbar.grid(row=0, column=1, sticky="ns")

frame_lista.grid_rowconfigure(0, weight=1)
frame_lista.grid_columnconfigure(0, weight=1)

# --- Barra de estado ---
barra_estado = tk.Label(ventana, text="Listo", fg="black",
                        bg="#81A1C1", font=("Arial", 12))
barra_estado.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# --- Funciones de los botones ---


def añadir_pelicula():
    """Añade una película a la lista"""
    datos = [campos_info[c]["entry"].get().strip() for c in campos_info]
    if not all(datos):
        barra_estado.config(
            text="⚠️ Rellena todos los campos antes de añadir.")
        return
    pelicula_texto = " | ".join(datos)
    lista_tareas.insert(tk.END, pelicula_texto)
    barra_estado.config(text="✅ Película añadida correctamente.")
    for campo in campos_info.values():
        campo["entry"].delete(0, tk.END)


def modificar_pelicula():
    """Edita una película seleccionada"""
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="⚠️ Selecciona una película para modificar.")
        return

    datos = [campos_info[c]["entry"].get().strip() for c in campos_info]
    if not all(datos):
        barra_estado.config(
            text="⚠️ Rellena todos los campos antes de modificar.")
        return

    pelicula_texto = " | ".join(datos)
    index = seleccion[0]
    lista_tareas.delete(index)
    lista_tareas.insert(index, pelicula_texto)
    barra_estado.config(text="✏️ Película modificada correctamente.")


def eliminar_pelicula():
    """Elimina la película seleccionada"""
    seleccion = lista_tareas.curselection()
    if not seleccion:
        barra_estado.config(text="⚠️ Selecciona una película para eliminar.")
        return
    index = seleccion[0]
    lista_tareas.delete(index)
    barra_estado.config(text="🗑️ Película eliminada correctamente.")


# --- Frame: Botones ---
frame_botones = tk.Frame(ventana, bg="#88C0D0")
frame_botones.grid(row=2, column=2, padx=10, pady=10)

botones = [
    ("Añadir Película", añadir_pelicula),
    ("Modificar Película", modificar_pelicula),
    ("Eliminar Película", eliminar_pelicula)
]

for i, (texto, comando) in enumerate(botones):
    btn = tk.Button(frame_botones, text=texto, fg="black",
                    bg="#88C0D0", font=("Arial", 12), command=comando)
    btn.grid(row=0, column=i, padx=10, pady=5)

# --- Base de datos SQLite (solo creación de tabla) ---
conexion = sqlite3.connect('tareas.db')
cursor = conexion.cursor()

comando_sql = """
CREATE TABLE IF NOT EXISTS Tarea (
    id INTEGER PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha_limite TEXT,
    prioridad TEXT,
    completada INTEGER
)
"""
cursor.execute(comando_sql)
conexion.commit()
conexion.close()

print("Tabla 'Tarea' creada con éxito (si no existía ya).")

# --- Ejecución principal ---
if __name__ == "__main__":
    ventana.mainloop()
