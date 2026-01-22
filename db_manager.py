import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
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
        self.conexion.commit()

    def añadir_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad):
        self.cursor.execute("""
            INSERT INTO Peliculas
            VALUES (NULL, ?, ?, ?, ?, ?, ?)
        """, (nombre, descripcion, director, protagonista, valoracion, prioridad))
        self.conexion.commit()

    def actualizar_lista(self):
        self.cursor.execute("""
            SELECT * FROM Peliculas ORDER BY id
        """)
        return self.cursor.fetchall()

    def cargar_pelicula_seleccionada(self, id_pelicula):
        self.cursor.execute("""
            SELECT nombre, descripcion, director, protagonista, valoracion, prioridad
            FROM Peliculas WHERE id=?
        """, (id_pelicula,))
        return self.cursor.fetchone()

    def modificar_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, id_pelicula):
        self.cursor.execute("""
            UPDATE Peliculas
            SET nombre=?, descripcion=?, director=?, protagonista=?, valoracion=?, prioridad=?
            WHERE id=?
        """, (nombre, descripcion, director, protagonista, valoracion, prioridad, id_pelicula))
        self.conexion.commit()

    def eliminar_pelicula(self, id_pelicula):
        self.cursor.execute("DELETE FROM Peliculas WHERE id=?", (id_pelicula,))
        self.conexion.commit()

    def pelicula_existe_por_id(self, id_pelicula):
        self.cursor.execute("""
            SELECT id FROM Peliculas
            WHERE id = ?
        """, (id_pelicula,))

        return self.cursor.fetchone() is not None

    def close(self):
        self.conexion.commit()
        self.conexion.close()