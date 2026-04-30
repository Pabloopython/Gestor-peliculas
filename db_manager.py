import sqlite3

class DatabaseManager:

    def __init__(self, db_name):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            director TEXT,
            protagonista TEXT,
            valoracion TEXT,
            prioridad TEXT,
            imagen TEXT
        )
        """)
        self.conexion.commit()

        self.conexion.commit()

    def añadir_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, imagen):
        self.cursor.execute('''
            INSERT INTO peliculas (nombre, descripcion, director, protagonista, valoracion, prioridad, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, director, protagonista, valoracion, prioridad, imagen))

        self.conexion.commit()

    def modificar_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, imagen, id_pelicula):
        self.cursor.execute('''
            UPDATE peliculas
            SET nombre=?, descripcion=?, director=?, protagonista=?, valoracion=?, prioridad=?, imagen=?
            WHERE id=?
        ''', (nombre, descripcion, director, protagonista, valoracion, prioridad, imagen, id_pelicula))

        self.conexion.commit()

    def eliminar_pelicula(self, id_pelicula):
        self.cursor.execute('DELETE FROM peliculas WHERE id=?', (id_pelicula,))
        self.conexion.commit()

    def actualizar_lista(self):
        self.cursor.execute('SELECT * FROM peliculas')
        return self.cursor.fetchall()

    def cargar_pelicula_seleccionada(self, id_pelicula):
        self.cursor.execute('''
            SELECT nombre, descripcion, director, protagonista, imagen, valoracion, prioridad
            FROM peliculas WHERE id=?
        ''', (id_pelicula,))
        return self.cursor.fetchone()