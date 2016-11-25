class Vertice(object):
    '''Clase que representa a un vertice de un grafo'''

    def __init__(self, dato):
        '''Crea al vertice'''

        self.dato = dato
        self.adyacentes = {}
        self.incidentes = {} #solo interesa si el grafo es dirigido

    def grado_adyacencia(self):
        '''Devuelve el grado de adyacencia '''

        return len(self.adyacentes)

    def grado_incidencia(self, grafo_es_dirigido):
        '''Devuelve el grado de incidencia'''

        if grafo_es_dirigido:

            return len(self.incidentes)

        return len(self.adyacentes)

    def obtener_dato(self):
        '''Devuelve el dato almacenado'''

        return self.dato

    def actualizar_dato(self, dato_nuevo):
        '''Actualiza lo almacenado por el vertice'''

        self.dato = dato_nuevo
        
    def eliminar_incidencia(self, vecino, grafo_es_dirigido):
        '''Se elimina a 'vecino' de las incidencias sobre el vertice'''

        if not grafo_es_dirigido:
        
            raise ValueError

        self.incidentes.pop(vecino)

    def eliminar_adyacencia(self, vecino):
        '''Se elimina a 'vecino' de los vertices adyacentes del vertice'''

        self.adyacentes.pop(vecino)

    def agregar_adyacencia(self, hasta, peso):
        '''Agrega una nueva adyacencia al vertice con peso 'peso' y destino 'hasta' '''
    
        self.adyacentes[hasta] = peso
    
    def agregar_incidencia(self, desde, peso):
        '''Agrega una nueva incidencia al vertice con peso 'peso' y destino 'hasta' '''

        self.incidentes[desde] = peso

    def es_adyacente(self, vecino):
        '''Devuelve si 'vecino' se encuentra entre los adyacentes del vertice'''

        return vecino in self.adyacentes

    def obtener_costo_arista(self, vecino):
        '''Devuelve el costo de la arista hacia 'vecino' '''

        return self.adyacentes.get(vecino)

    def obtener_vertices_adyacentes(self):
        '''Devuelve una lista con los adyacentes al vertice'''        

        return [adyacente for adyacente in self.adyacentes]
    
    def obtener_vertices_incidentes(self):
        '''Devuelve una lista con los incidentes al vertice'''
       
        return [incidente for incidente in self.incidentes]
