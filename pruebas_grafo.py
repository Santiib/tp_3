# -*- coding: utf-8 -*-
from grafo import *
from utils_floyd_warshall import *
import collections
from print_test import *
def vertice_pertenece(vertice,grafo):
    '''Devuelve True si el vertice pertenece al grafo, si no, False'''

    if vertice in grafo:

        return True

    return False

def pruebas_grafo_no_dirigido():
    
    print "\n*******PRUEBAS GRAFO NO DIRIGIDO*********\n"
    ciudades = {"Buenos Aires":1, "Mar Del Plata":2, "Tandil": 3, "Neuquen": 4, "El Bolsón": 5}

    grafo_ciudades = Grafo()
    for ciudad in ciudades:
        
        grafo_ciudades[ciudad] = ciudades[ciudad] 
        
    agregados = {"Buenos Aires":0,"Mar Del Plata":0,"Tandil":0,"Neuquen":0,"El Bolsón":0}  
    ciudades_desconocidos = False   
    ciudad_valores_correctos = True
    for ciudad in grafo_ciudades:

        try:

            if ciudades[ciudad] is not grafo_ciudades[ciudad]:

                ciudad_valores_correctos = False
                break

            else:

                agregados[ciudad] += 1

        except KeyError:

            ciudades_desconocidos = True

    print_test("No hay elementos de más", ciudades_desconocidos == False)
    print_test("Se asignaron los valores correctos a las distintas ciudades", ciudad_valores_correctos == True)
    vertices_correctos = True
    for ciudad in agregados:

        if agregados[ciudad] != 1:

            vertices_correctos = False
            break

    print_test("Los elementos fueron agregados una unica vez", vertices_correctos == True)
    print_test("La cantidad de vertices del grafo es correcta",len(grafo_ciudades) == 5)

    valores_aristas = {("Buenos Aires","Mar Del Plata"):380,("Mar Del Plata","Buenos Aires"):380,("Neuquen","El Bolsón"):100,("El Bolsón","Neuquen"):100,("Buenos Aires","Tandil"):368,("Tandil","Buenos Aires"):368,("Mar Del Plata","Tandil"):50,
("Tandil","Mar Del Plata"):50,("Buenos Aires","Neuquen"):1100,("Neuquen","Buenos Aires"):1100}

    origen = 0
    destino = 1

    for ruta in valores_aristas:
   
        grafo_ciudades.agregar_arista(ruta[origen], ruta[destino], valores_aristas[ruta])
    
    adyacencias = {"Buenos Aires":["Mar Del Plata","Tandil","Neuquen"],"Neuquen":["El Bolsón","Buenos Aires"],"Mar Del Plata":["Tandil","Buenos Aires"],"Tandil":["Buenos Aires","Mar Del Plata"],"El Bolsón":["Neuquen"]}

    rutas_correctas = True

    for ciudad in grafo_ciudades:

        adyacentes = grafo_ciudades.adyacentes(ciudad)
        adyacencias_dato = adyacencias[ciudad]

        if collections.Counter(adyacentes) != collections.Counter(adyacencias_dato):

            rutas_correctas = False
            break

    print_test("Adyacencias correctas",rutas_correctas == True)
    print_test("Existe conexion entre todas las ciudades", grafo_ciudades.es_conexo() == True)
    grafo_ciudades["Sudafrica"] = 6
    grafo_ciudades["Botswana"] = 7
    grafo_ciudades.agregar_arista("Sudafrica","Botswana",8)
    print_test("Dejo de existir conexion entre todas las ciudades",grafo_ciudades.es_conexo() == False)

    costos_correctos = True

    for arista in valores_aristas:

        origen = arista[0]
        destino = arista[1]

        if grafo_ciudades.obtener_peso_arista(origen, destino) != valores_aristas[arista]:

            costos_correctos = False
            break

    print_test("Pesos de aristas correctos", costos_correctos == True)
    comp_conexas = [["Tandil","Buenos Aires","Mar Del Plata","Neuquen","El Bolsón"],["Sudafrica","Botswana"]]
    componentes_conexas = grafo_ciudades.componentes_conexas()
    componentes_correctas = True

    for componente in componentes_conexas:
        
        pertenece_a_una_componente = 0
    
        for componente_dato in comp_conexas:

            if collections.Counter(componente) == collections.Counter(componente_dato):

                pertenece_a_una_componente += 1 

                    
        if pertenece_a_una_componente != 1:
        
            componentes_correctas = False
            break
    
    print_test("Componentes conexas correctas", componentes_correctas == True) 
    grafo_ciudades["Tierra Del Fuego"] = 7
    grafo_ciudades.agregar_arista("El Bolsón","Tierra Del Fuego",300)
    grafo_ciudades.agregar_arista("Neuquen","Tierra Del Fuego",50)
    mejor_camino = grafo_ciudades.camino_minimo("Buenos Aires","Tierra Del Fuego")

     #bs as nequen 1100, neuquen el bolson 100, bolson t fuego 300 => bs as t fuego 1500
     #bs as neuquen 1100, neuquen tierra del fuego 50 => bs as t del fuego 1150
    camino_recomendado = ["Buenos Aires","Neuquen","Tierra Del Fuego"]
    print_test("Se ha recomendado el mejor camino de Buenos Aires a TDF",mejor_camino == camino_recomendado)

    grafo_ciudades.agregar_arista("Neuquen","Tierra Del Fuego",401) #=> mejor camino x bolson
    camino_recomendado = ["Buenos Aires","Neuquen","El Bolsón","Tierra Del Fuego"]
    mejor_camino = grafo_ciudades.camino_minimo("Buenos Aires","Tierra Del Fuego")
    print_test("Se ha recomendado el mejor camino de Buenos Aires a TDF",mejor_camino == camino_recomendado)

    grafo_ciudades.agregar_arista("Buenos Aires","Tierra Del Fuego",1102)

    camino_recomendado = ["Buenos Aires","Tierra Del Fuego"]
    mejor_camino = grafo_ciudades.camino_minimo("Buenos Aires","Tierra Del Fuego")
    print_test("Se ha recomendado el mejor camino de Buenos Aires a TDF",mejor_camino == camino_recomendado)

    mejor_camino = ["Buenos Aires"]
    camino_recomendado = grafo_ciudades.camino_minimo("Buenos Aires","Buenos Aires")
    print_test("El camino a si mismo es el mejor",mejor_camino == camino_recomendado)
    es_conexo = grafo_ciudades.es_conexo()
    print_test("El grafo no es conexo",es_conexo == False)
   
def encontrar_ciclo():

    print "\n****PRUEBAS BUSCAR CICLO******\n"
    g = Grafo()
    vertices = ["v1","v2","v3"]
    for v in vertices:

        g[v] = None

    g.agregar_arista("v1","v2")
    g.agregar_arista("v1","v3")
    print_test("No se encontro ciclo",g.buscar_ciclo() == None)
    g.agregar_arista("v2","v3")
    print_test("Se encontro ciclo",g.buscar_ciclo() != None)
    g["v4"] = None
    g.agregar_arista("v3","v4")
    print_test("Se encontro ciclo",g.buscar_ciclo() != None)
    g.borrar_arista("v2","v3")
    print_test("No se encontro ciclo",g.buscar_ciclo() == None)
    g.agregar_arista("v4","v2")
    print_test("Se encontro ciclo",g.buscar_ciclo() != None)
   
def pruebas_grafo_dirigido():

    print "\n*****PRUEBAS GRAFO DIRIGIDO*****\n"

    grafo_carrera = Grafo(True)
    print_test("Es dirigido",grafo_carrera.es_dirigido())
    materias = {
                "Algebra CBC":None ,"Analisis CBC":None ,"Fisica CBC":None,
                "Quimica CBC":None,"Sociedad y Estado":None,"IPC":None,
                "Algoritmos I":6,"Analisis II":8,"Algebra II":8,"Matematica Discreta":6,
                "Algoritmos II":6,"Algoritmos III":6,"Algoritmos IV":6
               }
    
    for materia in materias:

        creditos = materias[materia]
        grafo_carrera[materia] = creditos

    materias_cbc = ["Algebra CBC","Analisis CBC","Fisica CBC","Quimica CBC","Sociedad y Estado","IPC"]

    correlativas = {
                    "Algoritmos I": materias_cbc, 
                    "Analisis II": materias_cbc,
                    "Algebra II": materias_cbc,
                    "Matematica Discreta": materias_cbc,
                    "Algoritmos II": ["Algoritmos I"],
                    "Algoritmos III": ["Algoritmos II"],
                    "Algoritmos IV": ["Algoritmos III"]
                   }

    for materia in correlativas:
        
        lista_correlativas = correlativas[materia]
        for correlativa in lista_correlativas:
            
            grafo_carrera.agregar_arista(correlativa,materia)

    print_test("No puedo cursar primero Algoritmos III sin antes cursar Algoritmos II",grafo_carrera.obtener_peso_arista("Algoritmos III","Algoritmos II") == None)

    print_test("Algoritmos II tiene como correlativa a Algoritmos I",grafo_carrera.obtener_peso_arista("Algoritmos I","Algoritmos II") == 1)

    print_test("No puedo cursar Algoritmos II y luego Algoritmos I",grafo_carrera.obtener_peso_arista("Algoritmos II","Algoritmos I") == None)

    print_test("No puedo cursar Algoritmos I y luego Analisis CBC",grafo_carrera.obtener_peso_arista("Algoritmos I","Analisis CBC") == None)

    print_test("Algoritmos I tiene como correlativa a Analisis del CBC",grafo_carrera.obtener_peso_arista("Analisis CBC","Algoritmos I") == 1)


    

    recorrido_desde_an_cbc = {'Analisis CBC': None, 'Algoritmos IV': 'Algoritmos III',                 
                              'Algoritmos III': 'Algoritmos II', 'Analisis II': 'Analisis CBC',
                              'Algoritmos II': 'Algoritmos I', 'Algebra II': 'Analisis CBC',
                              'Matematica Discreta': 'Analisis CBC', 'Algoritmos I': 'Analisis CBC'}

    distancia_desde_an_cbc = {
                              'Analisis CBC': 0, 'Algoritmos IV': 4, 'Algoritmos III': 3,                            'Analisis II': 1, 'Algoritmos II': 2, 'Algebra II': 1,
                              'Matematica Discreta': 1, 'Algoritmos I': 1
                              }

    recorrido_bfs_ancbc = grafo_carrera.bfs("Analisis CBC")
    correlativas_ancbc = recorrido_bfs_ancbc[0]
    distancias_a_ancbc = recorrido_bfs_ancbc[1]

    correlativas_y_distancias_correctas = True

    for materia in correlativas_ancbc:

        if correlativas_ancbc[materia] != recorrido_desde_an_cbc[materia]:

            correlativas_y_distancias_correctas = False

        if distancias_a_ancbc[materia] != distancia_desde_an_cbc[materia]:

            correlativas_y_distancias_correctas = False

    print_test("Recorrido del grafo dirigido correcto",correlativas_y_distancias_correctas == True)

def pruebas_calcular_mst():

    #estas pruebas son basadas en el ejemplo de la pagina
    #http://www.ma.uva.es/~antonio/Industriales/Clase_07-08/LabM/Alg_Prim.pdf
    #ejemplo 40
    #y se agrego una componente conexa para verificar que genere el bosque de tendido minimo
    print "\n******Pruebas calcular MST******\n"
    g = Grafo()
    vertices = {"v1":1,"v2":2,"v3":3,"v4":4,"v5":5,"v6":6,"v7":7,"e1":1,"e2":2,"e3":3}
    #e1,e2 y e3 en otra componente conexa
    for v in vertices:
        g[v] = vertices[v]

    aristas = [("v1","v2",5),("v1","v4",5),("v2","v4",5),("v2","v6",3),("v2","v3",5),("v3","v7",2),("v3","v6",4),("v7","v6",5),("v6","v5",1),("v6","v4",3),("e1","e2",1),("e1","e3",1),("e2","e3",10)]

    for arista in aristas:
        origen,destino,peso = arista
        g.agregar_arista(origen,destino,peso)
    
    mst_g = g.mst()
    dato_peso_mst = 18 + 2  #18 primer componente conexa, 2 la segunda
    print_test("MST calculado correctamente",dato_peso_mst == mst_g.obtener_peso_total())

def pruebas_distancias_y_recorridos_minimos():

    print "\n***PRUEBAS FLOYD - WARSHALL***\n"
    grafo_tareas = Grafo(True)
    tareas_diarias = ["Cambiarme - Aseo", "Desayunar", "Ir al trabajo",
                     "Ir a la universidad", "Descansar llego el finde :D",
                     "Gimnasio","Siesta y merienda" ,"Correr", "Pasear al perro",
                     "Visitar pareja", "Viciar", "Estudiar", "Escuchar musica", 
                    "Cocinar", "Mantenimiento del hogar", "Mirar la tele"] 

    for tarea in tareas_diarias:

        grafo_tareas[tarea] = None
    
    aristas = [("Cambiarme - Aseo","Desayunar",1),("Cambiarme - Aseo","Ir al trabajo",5),
                ("Cambiarme - Aseo","Ir a la universidad",4),
                ("Desayunar","Ir al trabajo",2),("Desayunar","Ir a la universidad",3)
                ,("Cambiarme - Aseo", "Descansar llego el finde :D",1),
                 ("Desayunar", "Gimnasio", 2), ("Cambiarme - Aseo", "Gimnasio", 20),
                 ("Ir al trabajo", "Gimnasio", 10), ("Ir a la universidad", "Gimnasio", 8),
                 ("Ir a la universidad", "Siesta y merienda", 1),
                 ("Ir al trabajo", "Siesta y merienda", 1),
                 ("Siesta y merienda", "Gimnasio", 4), ("Siesta y merienda", "Correr", 3),
                 ("Siesta y merienda", "Pasear al perro", 1),
                 ("Siesta y merienda", "Estudiar", 6),
                 ("Siesta y merienda", "Visitar pareja", 2),
                 ("Siesta y merienda", "Viciar", 1),
                 ("Siesta y merienda","Escuchar musica", 1),
                 ("Siesta y merienda", "Mantenimiento del hogar", 6), 
                 ("Siesta y merienda","Mirar la tele", 1),
                 ("Ir al trabajo", "Visitar pareja",8) ,("Ir al trabajo", "Viciar", 7)
                ,("Ir al trabajo", "Pasear al perro", 7),
                 ("Ir al trabajo", "Escuchar musica", 1)]

    origen = 0
    destino = 1
    costo = 2
    for arista in aristas:

        grafo_tareas.agregar_arista(arista[origen] ,arista[destino], arista[costo])

    distancias,predecesores = grafo_tareas.floyd_warshall()
    algunos_datos_conocidos = {'Gimnasio': {'Gimnasio': 0, 'Escuchar musica': float("inf"), 'Cambiarme - Aseo': float("inf"), 'Descansar llego el finde :D': float("inf"), 'Estudiar': float("inf"), 'Desayunar': float("inf"), 'Correr': float("inf"), 'Viciar': float("inf"), 'Cocinar': float("inf"), 'Mirar la tele': float("inf"), 'Ir al trabajo': float("inf"), 'Pasear al perro': float("inf"), 'Visitar pareja': float("inf"), 'Siesta y merienda': float("inf"), 'Mantenimiento del hogar': float("inf"), 'Ir a la universidad': float("inf")}, 'Escuchar musica': {'Gimnasio': float("inf"), 'Escuchar musica': 0, 'Cambiarme - Aseo': float("inf"), 'Descansar llego el finde :D': float("inf"), 'Estudiar': float("inf"), 'Desayunar': float("inf"), 'Correr': float("inf"), 'Viciar': float("inf"), 'Cocinar': float("inf"), 'Mirar la tele': float("inf"), 'Ir al trabajo': float("inf"), 'Pasear al perro': float("inf"), 'Visitar pareja': float("inf"), 'Siesta y merienda': float("inf"), 'Mantenimiento del hogar': float("inf"), 'Ir a la universidad': float("inf")}, 'Cambiarme - Aseo': {'Gimnasio': 3, 'Escuchar musica': 4, 'Cambiarme - Aseo': 0, 'Descansar llego el finde :D': 1, 'Estudiar': 10, 'Desayunar': 1, 'Correr': 7, 'Viciar': 5, 'Cocinar': float("inf"), 'Mirar la tele': 5, 'Ir al trabajo': 3, 'Pasear al perro': 5, 'Visitar pareja': 6, 'Siesta y merienda': 4, 'Mantenimiento del hogar': 10, 'Ir a la universidad': 4}, 'Descansar llego el finde :D': {'Gimnasio': float("inf"), 'Escuchar musica': float("inf"), 'Cambiarme - Aseo': float("inf"), 'Descansar llego el finde :D': 0, 'Estudiar': float("inf"), 'Desayunar': float("inf"), 'Correr': float("inf"), 'Viciar': float("inf"), 'Cocinar': float("inf"), 'Mirar la tele': float("inf"), 'Ir al trabajo': float("inf"), 'Pasear al perro': float("inf"), 'Visitar pareja': float("inf"), 'Siesta y merienda': float("inf"), 'Mantenimiento del hogar': float("inf"), 'Ir a la universidad': float("inf")}}

    calculos_correctos = True
    for tarea in algunos_datos_conocidos:
    
        if not calculos_correctos:

            break

        for distintas_tareas in algunos_datos_conocidos[tarea]:

            if algunos_datos_conocidos[tarea][distintas_tareas] != distancias[tarea][distintas_tareas]: 

                calculos_correctos = False
                break

    print_test("Calculo de distancias minimas correcto", calculos_correctos == True)
    mejores_recorridos = [["Cambiarme - Aseo", "Desayunar", "Ir al trabajo", "Escuchar musica"],["Cambiarme - Aseo", "Desayunar", "Ir al trabajo","Siesta y merienda", "Viciar"],["Cambiarme - Aseo", "Desayunar", "Ir al trabajo", "Siesta y merienda", "Mirar la tele"],
    ['Cambiarme - Aseo', 'Desayunar', 'Gimnasio'], ['Cambiarme - Aseo', 'Desayunar', 'Ir al trabajo', 'Siesta y merienda', 'Mantenimiento del hogar'], ['Cambiarme - Aseo', 'Ir a la universidad']]
    
    mejor_recorrido1 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Escuchar musica",list())
    mejor_recorrido2 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Viciar",list())
    mejor_recorrido3 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Mirar la tele", list())
    mejor_recorrido4 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Gimnasio",list())
    mejor_recorrido5 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Mantenimiento del hogar", list())
    mejor_recorrido6 = buscar_recorrido("Cambiarme - Aseo", predecesores, "Ir a la universidad", list())
    print_test("Recorrido 1 floyd warshall",mejor_recorrido1 == mejores_recorridos[0])
    print_test("Recorrido 2 floyd warshall",mejor_recorrido2 == mejores_recorridos[1])
    print_test("Recorrido 3 floyd warshall",mejor_recorrido3 == mejores_recorridos[2])
    print_test("Recorrido 4 floyd warshall",mejor_recorrido4 == mejores_recorridos[3])
    print_test("Recorrido 5 floyd warshall",mejor_recorrido5 == mejores_recorridos[4])
    print_test("Recorrido 6 floyd_warshall",mejor_recorrido6 == mejores_recorridos[5])
    diametro_dato_largo = 10
    diametro_dato_origen = "Cambiarme - Aseo"
    diametro_dato_fin = "Estudiar"
    print_test("Largo del diametro", grafo_tareas.diametro_largo() == diametro_dato_largo)
    print_test("Origen del diametro", grafo_tareas.diametro_origen() == diametro_dato_origen)
    print_test("Fin del diametro", grafo_tareas.diametro_fin() == diametro_dato_fin)
    diametro_camino = ['Cambiarme - Aseo', 'Desayunar', 'Ir al trabajo', 'Siesta y merienda', 'Estudiar']
    recorrido_diametro = buscar_recorrido(diametro_dato_origen, predecesores, diametro_dato_fin, list())
    print_test("El recorrido del diametro es correcto",recorrido_diametro == diametro_camino)
    print_test("Con dijkstra me devuelve el mismo camino",grafo_tareas.camino_minimo(diametro_dato_origen,diametro_dato_fin) == diametro_camino)

def grafo_discreta():
    print ("\n###GRAFO DISCRETA####\n")
    grafo = Grafo(False)
    vertices = {"v1":[("v2",2),("v9",7),("v8",6)],"v2":[("v9",4),("v3",4)],"v3":[("v9",2),("v4",3)],"v4":[("v9",1),("v5",5)],"v5":[("v9",8),("v6",2)],"v6":[("v9",5),("v7",4)],"v7":[("v9",4),("v8",3)],"v8":[("v9",2)],"v9":[]}
    for vertice in vertices:
        grafo[vertice] = None
    adyacente = 0
    peso = 1
    for vertice in vertices:
        for aristas in vertices[vertice]:
            grafo.agregar_arista(vertice, aristas[adyacente], aristas[peso])
    mst = grafo.mst()
    print mst.peso_total
            
def main():

    pruebas_grafo_no_dirigido()
    pruebas_calcular_mst()
    pruebas_grafo_dirigido()
    encontrar_ciclo()
    pruebas_distancias_y_recorridos_minimos()
    grafo_discreta()

main()
