import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import DatabaseManager
import os


class App:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Gestor de películas")
        self.ventana.geometry("700x700")
        self.ventana.configure(bg="#2E3440")

        style = ttk.Style()
        style.theme_use("clam")

        self.db = DatabaseManager('peliculas_gestor.db')
        self.db.crear_tabla()
        self.id_pelicula_seleccionada = None
        self.peliculas_cache = []

        self.frame_centrado = tk.Frame(self.ventana, bg="#2E3440")
        self.frame_centrado.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_formulario = tk.Frame(self.frame_centrado, bg="#2E3440")
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10)

        # 🔥 CAMPOS (AÑADIDO CATEGORÍA)
        self.campos_info = {
            "Nombre": {},
            "Descripción": {},
            "Director": {},
            "Protagonista": {},
            "Imagen": {},
            "Categoría": {}
        }

        for idx, etiqueta in enumerate(self.campos_info.keys()):
            lbl = tk.Label(self.frame_formulario, text=f"{etiqueta}:",
                           fg="black", bg="#D3D3D3", font=("Arial", 12))
            entry = tk.Entry(self.frame_formulario, width=50)

            lbl.grid(row=idx+1, column=2, padx=5, pady=5, ipady=5)
            entry.grid(row=idx+1, column=3, padx=5, pady=5, ipady=5)

            self.campos_info[etiqueta]["entry"] = entry

        # Valoración
        tk.Label(self.frame_formulario, text="Valoración:",
                 fg="black", bg="#D3D3D3", font=("Arial", 12)).grid(row=7, column=2)

        self.combo_valo = ttk.Combobox(
            self.frame_formulario,
            values=["1/5", "2/5", "3/5", "4/5", "5/5"],
            state="readonly"
        )
        self.combo_valo.grid(row=7, column=3)

        # Prioridad
        tk.Label(self.frame_formulario, text="Prioridad:",
                 fg="black", bg="#D3D3D3", font=("Arial", 12)).grid(row=8, column=2)

        self.combo_prio = ttk.Combobox(
            self.frame_formulario,
            values=["Baja", "Media", "Alta", "Urgente"],
            state="readonly"
        )
        self.combo_prio.grid(row=8, column=3)

        # Lista
        self.frame_lista = tk.Frame(self.frame_centrado)
        self.frame_lista.grid(row=1, column=0)

        self.lista_tareas = tk.Listbox(self.frame_lista, width=100, height=10)
        self.lista_tareas.grid(row=0, column=0)

        # Botones
        self.frame_botones = tk.Frame(self.frame_centrado, bg="#88C0D0")
        self.frame_botones.grid(row=2, column=0, pady=10)

        tk.Button(self.frame_botones, text="Añadir Película",
                  command=self.añadir_pelicula).grid(row=0, column=0, padx=10)

        tk.Button(self.frame_botones, text="Modificar Película",
                  command=self.modificar_pelicula).grid(row=0, column=1, padx=10)

        tk.Button(self.frame_botones, text="Eliminar Película",
                  command=self.eliminar_pelicula).grid(row=0, column=2, padx=10)

        self.lista_tareas.bind('<<ListboxSelect>>', self.cargar_seleccion)

        self.actualizar_lista()
        self.ventana.mainloop()

    # ---------------- AÑADIR ----------------
    def añadir_pelicula(self):
        datos = [self.campos_info[c]["entry"].get() for c in self.campos_info]

        self.db.añadir_pelicula(
            datos[0], datos[1], datos[2], datos[3],
            self.combo_valo.get(),
            self.combo_prio.get(),
            datos[4],  # imagen
            datos[5]   # categoria
        )

        self.actualizar_lista()

    # ---------------- MODIFICAR ----------------
    def modificar_pelicula(self):
        if self.id_pelicula_seleccionada is None:
            messagebox.showwarning("Error", "Selecciona una película primero")
            return

        datos = [self.campos_info[c]["entry"].get() for c in self.campos_info]

        self.db.modificar_pelicula(
            datos[0], datos[1], datos[2], datos[3],
            self.combo_valo.get(),
            self.combo_prio.get(),
            datos[4],  # imagen
            datos[5],  # categoria
            self.id_pelicula_seleccionada
        )

        self.actualizar_lista()

    # ---------------- ELIMINAR ----------------
    def eliminar_pelicula(self):
        if self.id_pelicula_seleccionada:
            self.db.eliminar_pelicula(self.id_pelicula_seleccionada)
            self.actualizar_lista()

    # ---------------- CARGAR ----------------
    def cargar_seleccion(self, event):
        if not self.lista_tareas.curselection():
            return

        index = self.lista_tareas.curselection()[0]
        pelicula = self.peliculas_cache[index]

        self.id_pelicula_seleccionada = pelicula[0]

        self.campos_info["Nombre"]["entry"].insert(0, pelicula[1])
        self.campos_info["Descripción"]["entry"].insert(0, pelicula[2])
        self.campos_info["Director"]["entry"].insert(0, pelicula[3])
        self.campos_info["Protagonista"]["entry"].insert(0, pelicula[4])
        self.campos_info["Imagen"]["entry"].insert(0, pelicula[7] or "")
        self.campos_info["Categoría"]["entry"].insert(0, pelicula[8] or "")

        self.combo_valo.set(pelicula[5])
        self.combo_prio.set(pelicula[6])

    # ---------------- LISTA ----------------
    def actualizar_lista(self):
        self.lista_tareas.delete(0, tk.END)

        self.peliculas_cache = self.db.actualizar_lista()

        for p in self.peliculas_cache:
            img = os.path.basename(p[7]) if p[7] else ""
            cat = p[8] if p[8] else ""

            self.lista_tareas.insert(
                tk.END,
                f"{p[1]} | {p[2]} | {p[3]} | {p[4]} | {img} | {cat} | {p[5]} | {p[6]}"
            )


if __name__ == "__main__":
    App()