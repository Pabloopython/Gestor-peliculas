import sqlite3


class DatabaseManager:

    def __init__(self, db_name):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()
        # Crear la tabla y aplicar migraciones (si procede)
        # Se delega al método crear_tabla para compatibilidad con el GUI
        self.crear_tabla()

    def crear_tabla(self):
        """Crea la tabla `peliculas` si no existe y aplica migraciones simples.


        Esto asegura que la base de datos esté siempre actualizada con los campos necesarios.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS peliculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                descripcion TEXT,
                director TEXT,
                protagonista TEXT,
                valoracion TEXT,
                prioridad TEXT
            )
        ''')

        # 🔥 MIGRACIONES AUTOMÁTICAS
        self.cursor.execute("PRAGMA table_info(peliculas)")
        columnas = [col[1] for col in self.cursor.fetchall()]

        if "imagenes" not in columnas:
            self.cursor.execute("ALTER TABLE peliculas ADD COLUMN imagenes TEXT")

        if "categoria" not in columnas:
            self.cursor.execute("ALTER TABLE peliculas ADD COLUMN categoria TEXT")

        self.conexion.commit()

    def añadir_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, imagenes, categoria):
        self.cursor.execute('''
            INSERT INTO peliculas (nombre, descripcion, director, protagonista, valoracion, prioridad, imagenes, categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, director, protagonista, valoracion, prioridad, imagenes, categoria))

        self.conexion.commit()

    def modificar_pelicula(self, nombre, descripcion, director, protagonista, valoracion, prioridad, imagenes, categoria, id_pelicula):
        self.cursor.execute('''
            UPDATE peliculas
            SET nombre=?, descripcion=?, director=?, protagonista=?, valoracion=?, prioridad=?, imagenes=?, categoria=?
            WHERE id=?
        ''', (nombre, descripcion, director, protagonista, valoracion, prioridad, imagenes, categoria, id_pelicula))

        self.conexion.commit()

    def eliminar_pelicula(self, id_pelicula):
        self.cursor.execute('DELETE FROM peliculas WHERE id=?', (id_pelicula,))
        self.conexion.commit()

    def actualizar_lista(self):
        self.cursor.execute('SELECT * FROM peliculas')
        return self.cursor.fetchall()

    def cargar_pelicula_seleccionada(self, id_pelicula):
        self.cursor.execute('''
            SELECT nombre, descripcion, director, protagonista, imagenes, categoria, valoracion, prioridad
            FROM peliculas WHERE id=?
        ''', (id_pelicula,))
        return self.cursor.fetchone()