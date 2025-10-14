class Película:

    def __init__(self, nombre, descripcion, director, protagonista, valoracion, prioridad=True, completada=False):
        
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
        return f"Nombre: {self.nombre} \nDescripcion: {self.descripcion} \nDirector: {self.director} \nProtagonista: {self.protagonista} \nValoracion: {self.valoracion} \nPrioridad: {self.prioridad} \nCompletada: {self.completada}"


película1=Película("Cars", "Infantil/Comedia", "John Lasseter", "Rayo Mcqueen", "5 estrellas", "Alta")
película2=Película("The Notebook", "Romance", "Nick Cassavetes", "Ryan Gosling", "5 estrellas", "Alta")

print("\n--- DATOS DE LA PELÍCULA 1 ---")
print(película1)
print("\n--- DATOS DE LA PELÍCULA 2 ---")
print(película2)