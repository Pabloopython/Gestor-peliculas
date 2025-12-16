import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        # Abre o crea la base de datos
        self.conexion = sqlite3.connect(db_path)

        # Crea un cursor que permite ejecutar comandos SQL
        self.cursor = self.conexion.cursor()

        # Llama al método que crea la tabla si no existe
        self.crear_tabla()

    def crear_tabla(self):
        # Crea la tabla "Peliculas" solo si no existe ya
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nombre TEXT NOT NULL,                 
            descripcion TEXT, 
            director TEXT,                                         
            protagonista TEXT,                     
            valoracion TEXT,                      
            prioridad TEXT                         
        )
        """)
        self.conexion.commit()   # Guarda cambios en la BD

    def añadir_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad):
        # Inserta una nueva película en la tabla
        self.cursor.execute("""
            INSERT INTO Peliculas
            (nombre, descripcion, director, protagonista, valoracion, prioridad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, descripcion, director, protagonista, valoracion, prioridad))

        self.conexion.commit()  # Guarda cambios

    def actualizar_lista(self):
        # Recupera todas las películas ordenadas por su ID
        self.cursor.execute("""
            SELECT id, nombre, descripcion, director, protagonista, valoracion, prioridad
            FROM Peliculas
            ORDER BY id
        """)
        return self.cursor.fetchall()  # Devuelve una lista de tuplas

    def cargar_pelicula_seleccionada(self, id_pelicula):
        # Recupera los datos de una película concreta a partir de su ID
        self.cursor.execute("""
            SELECT nombre, descripcion, director, protagonista, valoracion, prioridad
            FROM Peliculas
            WHERE id = ?
        """, (id_pelicula,))

        return self.cursor.fetchone()  # Devuel++e solo una fila

    def modificar_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, id_pelicula):
        # Actualiza los datos de una película existente
        self.cursor.execute("""
            UPDATE Peliculas
            SET nombre=?, descripcion=?, director=?, protagonista=?, valoracion=?, prioridad=?
            WHERE id=?
        """, (nombre, descripcion, director, protagonista, valoracion, prioridad, id_pelicula))

        self.conexion.commit()   # Guarda cambios


    def eliminar_pelicula(self, id_pelicula):
        # Elimina una película según su ID
        self.cursor.execute("""
            DELETE FROM Peliculas WHERE id = ?
        """, (id_pelicula,))

        self.conexion.commit()   # Guarda cambios
