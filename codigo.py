import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_manager import DatabaseManager
import json
# with open

class App:

    def __init__(self):
        # --- Ventana Principal ---
        self.ventana = tk.Tk()
        self.ventana.title("Gestor de películas")
        self.ventana.geometry("700x700")
        self.ventana.configure(bg="#2E3440")
        style = ttk.Style()
        style.theme_use("clam")

        self.db = DatabaseManager('peliculas_gestor.db')
        self.id_pelicula_seleccionada = None

        self.frame_centrado = tk.Frame(self.ventana, bg="#2E3440")
        self.frame_centrado.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_superior = tk.Frame(self.ventana, bg="#2E3440")
        self.frame_superior.pack(side="top", fill="x", pady=10)

        # --- Frame formulario ---
        self.frame_formulario = tk.Frame(self.frame_centrado, bg="#2E3440")
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10)

        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        # Menú Archivo
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Cerrar página", menu=menu_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(
            label="Exportar a JSON", command=self.exportar_json)
        menu_archivo.add_command(
            label="Importar desde JSON", command=self.importar_json)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)

        # Menú Ayuda
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Uso del programa",
                               command=self.mostrar_acerca_de)

        # Menú Creadores
        menu_creadores = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Creadores", menu=menu_creadores)
        menu_creadores.add_separator()
        menu_creadores.add_command(label="Alejandro Muñoz", state="disabled")
        menu_creadores.add_command(label="Pablo Chacón", state="disabled")
        menu_creadores.add_command(label="Álvaro Rodríguez", state="disabled")

        # Obtener premium
        menu_premium = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Premium", menu=menu_premium)
        menu_premium.add_command(
            label="Obtener Premium", command=self.obtener_premium)

        # Buscar palabra
        tk.Button(self.frame_superior, text="Mostrar todo",
                  command=self.actualizar_lista).pack(side="right", padx=5)

        tk.Button(
            self.frame_superior, text="Buscar",
            command=self.buscar_pelicula).pack(side="right", padx=5)

        self.entry_buscar = tk.Entry(self.frame_superior, width=40)
        self.entry_buscar.pack(side="right", padx=5)

        tk.Label(self.frame_superior, text="Buscar:", fg="black",
                 bg="#D3D3D3", font=("Arial", 12)).pack(side="right", padx=5)

        # --- Campos ---
        self.campos_info = {
            "Nombre": {},
            "Descripción": {},
            "Director": {},
            "Protagonista": {}
        }

        for idx, etiqueta in enumerate(self.campos_info.keys()):
            lbl = tk.Label(
                self.frame_formulario,
                text=f"{etiqueta}:",
                fg="black",
                bg="#D3D3D3",
                font=("Arial", 12)
            )
            entry = tk.Entry(self.frame_formulario, width=50)

            lbl.grid(row=idx+1, column=2, padx=5, pady=5, ipady=5)
            entry.grid(row=idx+1, column=3, padx=5, pady=5, ipady=5)

            self.campos_info[etiqueta]["entry"] = entry

        # Valoración
        tk.Label(self.frame_formulario, text="Valoración:", fg="black",
                 bg="#D3D3D3", font=("Arial", 12)).grid(row=5, column=2, padx=5, pady=5)
        self.combo_valo = ttk.Combobox(
            self.frame_formulario,
            values=["1/5", "2/5", "3/5", "4/5", "5/5"],
            state="readonly"
        )
        self.combo_valo.grid(row=5, column=3, padx=5, pady=5)

        # Prioridad
        tk.Label(self.frame_formulario, text="Prioridad:", fg="black",
                 bg="#D3D3D3", font=("Arial", 12)).grid(row=6, column=2, padx=5, pady=5)
        self.combo_prio = ttk.Combobox(
            self.frame_formulario,
            values=["Baja", "Media", "Alta", "Urgente"],
            state="readonly"
        )
        self.combo_prio.grid(row=6, column=3, padx=5, pady=5)

        # --- Lista ---
        self.frame_lista = tk.Frame(self.frame_centrado)
        self.frame_lista.grid(row=1, column=0, padx=10, pady=5)

        self.lista_tareas = tk.Listbox(self.frame_lista, width=100, height=10)
        self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical",
                                      command=self.lista_tareas.yview)
        self.lista_tareas.config(yscrollcommand=self.scrollbar.set)

        self.lista_tareas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Botones ---
        self.frame_botones = tk.Frame(self.frame_centrado, bg="#88C0D0")
        self.frame_botones.grid(row=2, column=0, padx=10, pady=10)

        botones = [
            ("Añadir Película", self.añadir_pelicula),
            ("Modificar Película", self.modificar_pelicula),
            ("Eliminar Película", self.eliminar_pelicula)
        ]

        for i, (texto, comando) in enumerate(botones):
            btn = tk.Button(
                self.frame_botones,
                text=texto,
                fg="black",
                bg="#88C0D0",
                font=("Arial", 12),
                command=comando
            )
            btn.grid(row=0, column=i, padx=10, pady=5)

        self.lista_tareas.bind('<<ListboxSelect>>', self.cargar_seleccion)

        self.actualizar_lista()
        self.ventana.mainloop()

    # ---------- BÚSQUEDA ----------
    def buscar_pelicula(self):
        palabra = self.entry_buscar.get().lower().strip()

        self.lista_tareas.delete(0, tk.END)
        self.peliculas_cache = []

        for p in self.db.actualizar_lista():
            texto = f"{p[1]} {p[2]} {p[3]} {p[4]}".lower()

            if palabra in texto:
                self.lista_tareas.insert(
                    tk.END,
                    f"{p[1]} | {p[2]} | {p[3]} | {p[4]} | {p[5]} | {p[6]}"
                )
                self.peliculas_cache.append(p[0])

    # ---------- AYUDA ----------
    def mostrar_acerca_de(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Información del Gestor")
        ventana.geometry("615x250")
        ventana.grab_set()
        ventana.transient(self.ventana)

        tk.Label(ventana, text="Gestor de Películas").pack(pady=20)
        tk.Label(ventana, text="Permite guardar películas para ver más tarde.").pack()
        tk.Label(
            ventana, text="Puedes añadir, modificar o eliminar películas.").pack()
        tk.Button(ventana, text="Cerrar",
                  command=ventana.destroy).pack(pady=20)

    # ---------- PREMIUM ----------
    def obtener_premium(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Obtener Premium")
        ventana.geometry("800x500")
        ventana.grab_set()
        ventana.transient(self.ventana)
        style = ttk.Style()
        style.theme_use("clam")

        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=30)

        tk.Label(ventana, text="¡Gracias por tu interés en obtener Premium!",  fg="black", font=("Arial", 21)).pack(
            pady=20)
        tk.Label(ventana, text="¿Qué ventajas ofrece Premium?", fg="black", font=("Arial", 17, "italic")).pack(
            pady=20)
        tk.Label(ventana, text="    Numero ilimitados de películas guardadas",
                 fg="black", font=("Arial", 14)).pack()
        tk.Label(
            ventana, text="    Guardar películas sin necesidadad de tener cobertura", fg="black", font=("Arial", 14)).pack()
        tk.Label(ventana, text="    Libre de anuncios",
                 fg="black", font=("Arial", 14)).pack()

        ttk.Button(frame_botones, text="Comprar Premium", command=self.cp).grid(
            row=0, column=0, padx=20)

        ttk.Button(frame_botones, text="Plan Familiar", command=self.pf).grid(
            row=0, column=1, padx=20)

        tk.Button(ventana, text="Cerrar",
                  command=ventana.destroy).pack(pady=20)

    def cp(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Comprar Premium")
        ventana.geometry("400x200")
        ventana.grab_set()
        ventana.transient(self.ventana)
        style = ttk.Style()
        style.theme_use("clam")

        tk.Label(ventana, text="Ahora mismo se encuentra en mantenimiento,", fg="black", font=("Arial", 11)).pack(
            padx=25)
        tk.Label(ventana, text="disculpe las molestias.", fg="black", font=("Arial", 11)).pack(
            padx=5)

    def pf(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Plan Familiar")
        ventana.geometry("400x200")
        ventana.grab_set()
        ventana.transient(self.ventana)
        style = ttk.Style()
        style.theme_use("clam")

        tk.Label(ventana, text="Ahora mismo se encuentra en mantenimiento,", fg="black", font=("Arial", 11)).pack(
            padx=25)
        tk.Label(ventana, text="disculpe las molestias.", fg="black", font=("Arial", 11)).pack(
            padx=5)

    # ---------- JSON ----------

    def exportar_json(self):
        peliculas = self.db.actualizar_lista()

        datos = []
        for p in peliculas:
            datos.append({
                "id": p[0],
                "nombre": p[1],
                "descripcion": p[2],
                "director": p[3],
                "protagonista": p[4],
                "valoracion": p[5],
                "prioridad": p[6]
            })

        with open(filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")]), "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Exportación", "Datos exportados correctamente")

    def importar_json(self):
        try:
            with open(filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")]), "r", encoding="utf-8") as f:
                peliculas = json.load(f)

            for p in peliculas:
                if not self.db.pelicula_existe_por_id(p["id"]):
                    self.db.añadir_pelicula(
                        p["nombre"],
                        p["descripcion"],
                        p["director"],
                        p["protagonista"],
                        p["valoracion"],
                        p["prioridad"]
                    )

            self.actualizar_lista()
            messagebox.showinfo(
                "Importación", "Datos importados correctamente")

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo JSON")

    # ---------- Métodos ----------
    def añadir_pelicula(self):
        datos = [c["entry"].get().strip() for c in self.campos_info.values()]
        self.db.añadir_pelicula(
            *datos, self.combo_valo.get(), self.combo_prio.get())
        self.actualizar_lista()

    def modificar_pelicula(self):
        if not self.id_pelicula_seleccionada:
            return
        datos = [c["entry"].get().strip() for c in self.campos_info.values()]
        self.db.modificar_pelicula(*datos, self.combo_valo.get(),
                                   self.combo_prio.get(), self.id_pelicula_seleccionada)
        self.actualizar_lista()

    def eliminar_pelicula(self):
        if not self.id_pelicula_seleccionada:
            return
        self.db.eliminar_pelicula(self.id_pelicula_seleccionada)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_tareas.delete(0, tk.END)
        self.peliculas_cache = []

        for p in self.db.actualizar_lista():
            self.lista_tareas.insert(
                tk.END,
                f"{p[1]} | {p[2]} | {p[3]} | {p[4]} | {p[5]} | {p[6]}"
            )
            self.peliculas_cache.append(p[0])

    def cargar_seleccion(self, event):
        if not self.lista_tareas.curselection():
            return

        index = self.lista_tareas.curselection()[0]
        self.id_pelicula_seleccionada = self.peliculas_cache[index]
        datos = self.db.cargar_pelicula_seleccionada(
            self.id_pelicula_seleccionada)

        for campo, valor in zip(self.campos_info.values(), datos[:4]):
            campo["entry"].delete(0, tk.END)
            campo["entry"].insert(0, valor)

        self.combo_valo.set(datos[4])
        self.combo_prio.set(datos[5])


if __name__ == "__main__":
    app = App()


# Esto es una prueba
