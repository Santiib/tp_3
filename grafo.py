# -*- coding: utf-8 -*-
import Queue
from utils_grafo import *
from vertice import *

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''

        self.dirigido = es_dirigido
        self.cantidad_vertices = 0
        self.vertices = {} #Id:vertice
        self.aristas = 0 #para calcular mst
        self.peso_total = 0
        self.distancias_minimas = None
        self.predecesores_caminos_minimos = None
        self.diametro = 0
        self.origen_diametro = None
        self.fin_diametro = None

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''

        return self.cantidad_vertices
    
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''

        for vertice in self.vertices:

            yield vertice
        
    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''

        return [k for k in self.vertices]

    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
        
        return self.vertices[id].obtener_dato()

    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
        '''

        if id in self.vertices:

            self.vertices[id].actualizar_dato(valor)

        else:
            nuevo_vertice = Vertice(valor)
            self.vertices[id] = nuevo_vertice
            self.cantidad_vertices += 1
    
    def __delitem__(self, id):
        '''Elimina el vertice del grafo, y devuelve el valor asociado. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        dato = obtener_dato(self.vertices[id])
        
        adyacentes = self.vertices[id].adyacentes.keys()
        for adyacente in adyacentes:

            self._borrar_arista(id,adyacente,1) 
            if self.dirigido:

                self.vertices[adyacente].eliminar_incidencia(id, self)

        self.vertices.pop(id)
        self.cantidad_vertices-=1
        return dato
        
    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''

        return id in self.vertices

    def es_dirigido(self):
        '''Devuelve si el grafo es dirigido o no'''
        
        return self.dirigido
        
    def incidencias(self,id):
        '''Devuelve los vertices incidentes sobre el vertice 'id', lanza ValueError
           si el grafo es dirigido'''

        if not self.dirigido:
        
            raise ValueError

        return self.vertices[id].obtener_vertices_incidentes()

    def obtener_peso_total(self):
        '''Devuelve la sumatoria de los pesos de las aristas del grafo'''

        return self.peso_total

    def _agregar_arista(self, desde, hasta, peso, recursion):
        '''Agrega una arista al grafo, comenzando en <desde>' y culminando en
           <hasta>, con peso <peso>, <recursion> se utiliza por si el grafo es
            no dirigido y hay que agregar la arista recíproca'''
        
        if recursion > 1:

            self.aristas+=1 
            self.peso_total+=peso
            return

        nueva_arista = (desde,hasta)                
        self.vertices[desde].agregar_adyacencia(hasta, peso)

        if not self.dirigido:

            self._agregar_arista(hasta,desde,peso,recursion+1)

        else:

            self.aristas+=1 
            self.peso_total += peso
            self.vertices[hasta].agregar_incidencia(desde, peso)


    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        if self.vertices[desde].es_adyacente(hasta):

            self.vertices[desde].agregar_adyacencia(hasta, peso)

            if not self.dirigido:

                self.vertices[hasta].agregar_adyacencia(desde, peso)
            
            else:

                self.vertices[hasta].agregar_incidencia(desde, peso)

            return

        self._agregar_arista(desde, hasta, peso, 0)
        
    def _borrar_arista(self,desde,hasta,paso_recursivo):

        '''Borra una arista del grafo, que comience en <desde>, culmine en 
           <hasta>, y ademas, el parametro <paso_recursivo> se utiliza por si
           hay que borrar la arista reciproca por si se esta en un grafo dirigido'''

        if paso_recursivo > 1 or (paso_recursivo == 1 and desde == hasta): #En el caso de que este en un grafo no dirigido, o con un lazo
            return

        if self.vertices[hasta] and self.vertices[desde]:

            try:
               
               self.vertices[desde].eliminar_adyacencia(hasta)

            except KeyError:

                raise ValueError

        if not self.dirigido:

            self._borrar_arista(hasta,desde,paso_recursivo+1)

        else:

            self.vertices[hasta].eliminar_incidencia(desde, self)      
                
    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        recursion = 0
        self._borrar_arista(desde,hasta,recursion)

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if self.vertices[hasta] and self.vertices[desde]:

            return self.vertices[desde].obtener_costo_arista(hasta)
       
    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''

        vertice = self.vertices[id]
        return vertice.obtener_vertices_adyacentes()

    def grado_adyacencia_vertice(self, id):
        '''Devuelve el grado de adyacenci adel vertice 'id',
           si no se encuentra, lanza KeyError'''
        return self.vertices[id].grado_adyacencia()

    def grado_incidencia_vertice(self, id):
        '''Devuelve el grado de incidencia del vertice 'id',
           si no se encuentra, lanza KeyError'''
        return self.vertices[id].grado_incidencia()

    def buscar_ciclo(self):
        'Busca un ciclo cualquiera en el grafo'

        vertices = self.vertices
        visitados = list()
        padres = dict()
        for vertice in vertices:

            if vertice not in visitados:

                padres[vertice] = None
                visitados.append(vertice)
                ciclo = hallar_ciclo(self, vertice, visitados, [vertice], padres)
                if ciclo:

                    break

        return ciclo
 
    def bfs(self, inicio=None, visitar = visitar_nulo, extra = None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        padre,orden = recorrido(self, recorrido_bfs, inicio, visitar, extra)   
        return padre,orden
        

    def dfs(self, inicio=None, visitar = visitar_nulo, extra = None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        padre,orden = recorrido(self, recorrido_dfs, inicio, visitar, extra)   
        return padre,orden
        
    def es_conexo(self):
        '''Devuelve True si el grafo es conexo, caso contrario, False'''

        return recorrido(self, recorrido_bfs, None, visitar_nulo, None, True)

    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''

        if self.dirigido:

            raise TypeError 

        lista_componentes_conexas = []
        self.bfs(None, obtener_componentes_conexas,lista_componentes_conexas)
        return lista_componentes_conexas

    def cantidad_aristas(self):
        '''Devuelve la cantidad de aristas que hay en el grafo'''
        
        return self.aristas

    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''

        if destino == origen:
            return [origen]

        vecinos = Queue.PriorityQueue()
        vecinos.put((0,origen))
        vuelta = dict()
        vuelta[origen] = None
        costos = dict()
        costos[origen] = 0
    
        while not vecinos.empty():

            costo,actual = vecinos.get()
           
            if actual == destino:
                break

            adyacentes_actual = self.adyacentes(actual)

            for vertice in adyacentes_actual:

                nuevo_costo = costos[actual] + self.obtener_peso_arista(actual,vertice)

                if vertice not in costos or nuevo_costo < costos[vertice]:

                    costos[vertice] = nuevo_costo
                    vecinos.put((nuevo_costo + heuristica(actual,destino),vertice))
                    vuelta[vertice] = actual

        if destino not in vuelta:
            return
        
        mejor_camino = [destino]
        construir_camino(vuelta, origen, destino, mejor_camino)
        return mejor_camino
        
    def mst(self):
        '''Calcula el Bosque de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        if self.dirigido:
            raise TypeError

        bosque_tendido_min = Grafo()      
        visitados = list()
        cantidad_aristas = 0

        for vertice in self:     

            bosque_tendido_min[vertice] = self[vertice] 

        for vertice in self:

            if vertice not in visitados:

                mst_prim(bosque_tendido_min, self, vertice, visitados, self.aristas, cantidad_aristas)
          
        return bosque_tendido_min 

    # Codigo python para el algoritmo de Floyd-Warshall
    # Adaptado del codigo que se encuentra en el modulo networkx
    def floyd_warshall(self):
        '''Aplica el algoritmo de Floyd - Warshall a el grafo, se devuelve
           un diccionario distancias, con claves como todos los vertices del grafo
           y valor otro diccionario donde las claves son, nuevamente, los vertices
           del grafo, y como valor, la distancia al vertice original.

           Tambien se devuelve un diccionario predecesores, con las mismas
           caracteristicas que el diccionario anterior, pero el valor de cada
           vertice en el segundo diccionario contendra el mejor vertice anterior
           a la clave actual para llegar al vertice que contiene al segundo 
           diccionario como clave''' 

        distancias = {}
        predecesores = {}
    
        # Ciclo de inicializacion
        # Para cada vertice del grafo, inicializa los caminos de ese vertice
        # a sus vecinos y a sus no vecinos.
        for vertice in self:  

            distancias[vertice] = {}
            predecesores[vertice] = {}
            vecinos = self.adyacentes(vertice)

            for posible_vecino in self:  

                if posible_vecino in vecinos:

                    distancias[vertice][posible_vecino] = self.obtener_peso_arista(vertice,posible_vecino)
                    predecesores[vertice][posible_vecino] = vertice

                else:
                    distancias[vertice][posible_vecino] = float("inf")
                    predecesores[vertice][posible_vecino] = None

            distancias[vertice][vertice] = 0  # inicializa en 0 la distancia a si mismo
    
    	# Ciclo de calculo
        for w in self:

            for u in self:

                for v in self:

                    if distancias[u][v] > distancias[u][w] + distancias[w][v]:

                        distancias[u][v] = distancias[u][w] + distancias[w][v]
                        predecesores[u][v] = predecesores[w][v]

        self.distancias_minimas = distancias
        self.predecesores_caminos_minimos = predecesores
        return distancias,predecesores

    def calcular_diametro(self):

        """ Calcula el diametro del grafo. 
            Pre: Se debe ejecutar en una instancia del grafo, si ya se ejecutó
            Floyd-Warshall, posteriormente no se debe haber modificado el grafo,
            si no los resultados podrian no ser los esperados.

            Post: Calcula el diametro, el origen y el fin del camino asociados al
            diametro y guarda esta informacion en el grafo. Si se ejecuta sin antes
            haber ejecutado el algoritmo de Floyd-Warshall, se ejecutara previamente"""

        distancia_maxima = 0
        origen = None
        destino = None
        peso_actual = 0
        
        if not self.distancias_minimas:

            self.floyd_warshall()

        recorridos_minimos = self.distancias_minimas
        for vertice in recorridos_minimos:

            for destino_vertice in recorridos_minimos[vertice]:

                distancia_actual = recorridos_minimos[vertice][destino_vertice]
                if distancia_actual > distancia_maxima and distancia_actual != float("inf"):
                    distancia_maxima = distancia_actual
                    origen = vertice
                    destino = destino_vertice
    
        self.diametro = distancia_maxima
        self.origen_diametro = origen
        self.fin_diametro = destino

    def diametro_largo(self):
        """ Devuelve el diametro. Si no fue calculado anteriormente,
            se calcula """
        
        if not self.diametro:
                
            self.calcular_diametro()

        return self.diametro

    def diametro_origen(self):

        """ Devuelve el origen del diametro. Si no fue calculado anteriormente,
            se calcula """

        if not self.diametro:

            self.calcular_diametro()

        return self.origen_diametro

    def diametro_fin(self):

        """ Devuelve el fin diametro. Si no fue calculado anteriormente,
            se calcula """

        if not self.diametro:

            self.calcular_diametro()

        return self.fin_diametro
