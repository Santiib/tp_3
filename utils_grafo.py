# -*- coding: utf-8 -*-8
from cola import *
import Queue

def recorrido(grafo, tipo_recorrido, inicio, visitar, extra, investigar_conexidad = False):

    '''Recorre el grafo segun el tipo de recorrido recibido,
       devuelve un diccionario padre que indica el padre de cada
       vertice para volver atras en el recorrido, orden que indica
       el orden de cada vertice en el recorrido
       opcionalmente, si se desea investigar la conexidad 
       devolvera True si es conexo, false si no.
    '''

    visitados = []
    padre = dict()
    orden = dict()
        
    if not inicio:

        componentes_conexas = 0
        for vertice in grafo:

            if vertice not in visitados:

                componentes_conexas+=1
                padre[vertice] = None
                orden[vertice] = 0
                tipo_recorrido(grafo, vertice, visitados, orden, padre, visitar, extra)
    else:

        padre[inicio] = None 
        orden[inicio] = 0

        tipo_recorrido(grafo, inicio, visitados, orden, padre, visitar, extra)

    if investigar_conexidad:

        if componentes_conexas > 1:
            return False

        return True

    return padre,orden


def recorrido_dfs(grafo, actual, visitados, orden, padre, visitar, extra):
    '''Recorrido DFS para un grafo, se aplicara la funcion
       visitar a cada vertice y se finalizara el recorrido
       si la funcion devuelve False, extra es un parametro para
       la funcion visitar, si es necesario'''

    continuar = visitar(actual, padre, orden, extra)

    if not continuar:

        return 

    visitados.append(actual)
    adyacentes = grafo.adyacentes(actual)

    for vertice in adyacentes:

        if vertice not in visitados :

            padre[vertice] = actual
            orden[vertice] = orden[actual] + 1
            recorrido_dfs(grafo, vertice, visitados, orden, padre, visitar, extra)

def recorrido_bfs(grafo, origen, visitados, orden, padre, visitar, extra):  
    '''Recorrido BFS para un grafo, se aplicara la funcion
       visitar a cada vertice y se finalizara el recorrido
       si la funcion devuelve False, extra es un parametro para
       la funcion visitar, si es necesario'''

    cola = Cola()
    cola.encolar(origen)
    visitados.append(origen)
        
    while not cola.esta_vacia():
            
        actual = cola.desencolar()
        continuar = visitar(actual, padre, orden, extra)

        if not continuar:

           return 

        adyacentes = grafo.adyacentes(actual)

        for vertice in adyacentes:

            if vertice not in visitados:

                visitados.append(vertice)
                padre[vertice] = actual
                orden[vertice] = orden[actual] + 1       
                cola.encolar(vertice)


def construir_camino(vertices_direcciones, origen, destino, camino):
    ''' Construye un camino desde 'destino' hasta  'origen' 
        vertices_direcciones es un diccionario que indica de
        donde vino el vertice actual, y camino es el camino
        actualizado hasta el momento'''

    anterior = vertices_direcciones[destino]
    camino.insert(0,anterior)

    if anterior == origen:
        return

    construir_camino(vertices_direcciones, origen, anterior, camino)

def mst_prim(arbol_tendido_min, grafo, origen, visitados, cantidad_aristas_limite, cantidad_aristas_actual):
    '''Genera el bosque de tendido minimo para un grafo mediante el
        algoritmo de prim'''

    cola_aristas = Queue.PriorityQueue()
    adyacentes_origen = grafo.adyacentes(origen)
    visitados.append(origen)
        
    for vertice in adyacentes_origen:
            
        peso_hasta_vertice = grafo.obtener_peso_arista(origen,vertice)
        cola_aristas.put((peso_hasta_vertice,vertice,origen))
        
    while not cola_aristas.empty() and cantidad_aristas_actual < cantidad_aristas_limite:         
        
        peso,hijo,padre = cola_aristas.get()
        if hijo not in visitados:
                
            visitados.append(hijo)
            arbol_tendido_min.agregar_arista(hijo,padre,peso)
            cantidad_aristas_actual += 1                
            adyacentes_hijo = grafo.adyacentes(hijo)
            for vertice in adyacentes_hijo:

                if vertice not in visitados:

                    peso_hasta_hijo = grafo.obtener_peso_arista(hijo,vertice)
                    cola_aristas.put((peso_hasta_hijo,vertice,hijo))

def obtener_componentes_conexas(vertice,padre,orden,lista_componentes):
    '''Utilidad para usar como funcion visitar en un recorrido BFS o DFS para
       obtener las distintas componentes conexas de un grafo'''

    if not padre[vertice]:
        lista_componentes.append([vertice])

    else:
        ultima_componente = len(lista_componentes) - 1
        lista_componentes[ultima_componente].append(vertice)    

    return True        


def buscar_ciclo_longitud_k(actual, padre, orden, extra):

    '''Funcion especificamente diseñada para usar como parametro <funcion
       a aplicar> en el recorrido DFS de un grafo.
      
       En este caso <extra> contiene al grafo, la longitud del ciclo deseado,
       el origen desde donde se desea que comience el ciclo y un elemento mas
       que guardara el ciclo si es que se encuentra.
       
       Busca un ciclo de cierta longitud que parta desde el origen
    '''

    contenedor_ciclo = 1
    longitud_ciclo = extra[0]
    grafo = extra[2]
    origen_ciclo = extra[3]    
    if orden[actual] < longitud_ciclo:

        return True

    adyacentes_actual = grafo.adyacentes(actual)
    if origen_ciclo in adyacentes_actual:

        ciclo = [actual]
        construir_camino(padre, origen_ciclo, actual, ciclo)
        ciclo.append(origen_ciclo)
        extra[contenedor_ciclo] = ciclo        

    return False

def hallar_ciclo(grafo, actual, visitados, ciclo, padres, finalizar = False):
    '''Busca un ciclo cualquiera en el grafo'''

    if finalizar:
        return ciclo
    hijos = grafo.adyacentes(actual)
    for hijo in hijos:
        padres[hijo] = actual
        if hijo in ciclo and hijo != padres[actual]:
            ciclo.append(hijo)
            return hallar_ciclo(grafo, hijo, visitados, ciclo, padres, True)
    
        elif hijo not in visitados:
            ciclo.append(hijo)
            visitados.append(hijo)
            return hallar_ciclo(grafo, hijo, visitados, ciclo, padres, False)

