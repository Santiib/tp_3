# -*- coding: utf-8 -*-
from grafo import *
import sys
import operator
import random
import math
'''import collections
from print_test import *'''

def cargar_archivo():
	#print ('Argument List:', str(sys.argv))
	try:
		#archivo = open((sys.argv),'r')   #falta implementar la lectura por consola
		archivo = open("marvel.pjk",'r')
		return archivo
	except IOError:
		raise IOError("no se reconocio el archivo")
		
def crear_grafo_y_dic_nombres(archivo):
	primer_linea = archivo.readline()
	
	palabras = []
	palabras = primer_linea.split(" ")
	
	cant_vertices = int(palabras[1])
	
	grafo = Grafo()
	nombres = {}  #es para saber el id correspondiente a los nombres ya que en los comandos se ingresan nombres
	
	for pos in range(0, cant_vertices):
		linea = archivo.readline()
		palabras = linea.split(" ")
		id = int(palabras.pop(0))
		nombre_personaje = ' '.join(palabras)
		nombre_personaje = nombre_personaje[1:-2] #saco comillas
		grafo[id] = nombre_personaje
		nombres[nombre_personaje] = id
		
	linea = archivo.readline()
	linea = archivo.readline()
	
	while(linea):
		palabras = linea.split(" ")
		vertice_origen = int(palabras[0])
		vertice_destino = int(palabras[1])
		peso = int(palabras[2])
		grafo.agregar_arista(vertice_origen, vertice_destino, peso)
		linea = archivo.readline()
	
	print("archivo leido")
	archivo.close()
	return grafo, nombres

def hacer_random_walk(grafo, nombres, vertice, cantidad, caminos, largo, pesado, recomendar):
	'''Realiza un random walk y devuelve los (cantidad) mas similares al vertice dado, si recomendar == True se omiten los vertices
	que sean adyacentes al dado.'''
	similitudes = grafo.random_walk(nombres, vertice, caminos, largo, pesado)
	similitudes_lista = sorted(similitudes.items(), key=operator.itemgetter(1)) #ordena de menor a mayor por similitud
	a_imprimir = []
	agregados = 0
	for v in similitudes_lista[::-1]:
		if v[0] == nombres[vertice]:
			continue
		if agregados == cantidad:
			break
		if recomendar:
			if v[0] in grafo.vertices[nombres[vertice]][1]: 
				continue
		a_imprimir.append(grafo.vertices[v[0]][0])
		agregados += 1
	return a_imprimir
	
def similares(grafo, nombres, vertice, cantidad, caminos, largo, pesado = True): #esta hecho teniendo en cuenta que vertice es el id y no el nombre/valor.
	if vertice not in nombres:
		raise KeyError('id no se encuentra en el grafo.')
	mas_similares = hacer_random_walk(grafo, nombres, vertice, cantidad, caminos, largo, pesado, False)
	print (', '.join(mas_similares))
	
def recomendar(grafo, nombres, vertice, cantidad, caminos, largo, pesado = True):
	if vertice not in nombres:
		raise KeyError('id no se encuentra en el grafo.')
	recomendaciones = hacer_random_walk(grafo, nombres, vertice, cantidad, caminos, largo, pesado, True)
	print (', '.join(recomendaciones))
	
def comunidades(grafo):
	labels = grafo.label_propagation()
	comunidades = {}
	for v in labels:
		if labels[v] in comunidades:
			comunidades[labels[v]].append(grafo[v])
		else:
			comunidades[labels[v]] = []
			comunidades[labels[v]].append(grafo[v])
	for comunidad in comunidades:
		if (len(comunidades[comunidad]) < 4) or (len(comunidades[comunidad]) > 1000):
			continue
		print ("")
		print ("Comunidad: "+str(comunidad))
		print ("Cantidad de integrantes: "+str(len(comunidades[comunidad])))
		print ("Integrantes:")
		print (comunidades[comunidad])
		
def estadisticas(grafo):
	grado_total = 0
	for v in grafo.vertices:
		grado_total += len(grafo.vertices[v][1])
	grado_promedio = grado_total/float(len(grafo.vertices))
	desvio_total = 0
	for v in grafo.vertices:
		desvio_total += (len(grafo.vertices[v][1])-grado_promedio)**2
	desvio_estandar = math.sqrt(desvio_total/(len(grafo.vertices)-1))
		
	print ("Cantidad de vertices: "+str(len(grafo.vertices)))
	print ("Cantidad de aristas: "+str(grafo.cant_aristas))
	print ("Promedio del grado de cada vertice: "+str(grado_promedio))
	print ("Desvio estandar del grado de cada vertice: "+str(desvio_estandar))
	print ("Densidad del grafo: "+str(2*grafo.cant_aristas/float((len(grafo.vertices)*(len(grafo.vertices)-1))))) #2*|E|/|V|*(|V|-1)
			
def camino(grafo, origen, destino):
	camin = grafo.camino_minimo(origen, destino, True)
	nombres_camino = []
	for id in camin:
		nombres_camino.append(grafo[id] + " ->")
	
	print(nombres_camino)

def ordenar_vertices(grafo, distancias):
	vertices_ordenados = []
	vertices_ordenados = sorted(distancias.items(), key=operator.itemgetter(1)) #ordena por valores (en este caso distancias)
	return vertices_ordenados[::-1]
	
def centralidad(grafo, cant_personajes):
	contador_apariciones_total = {}
	for ver in grafo.vertices:
		contador_apariciones_total[ver] = 0
	
	for v in grafo.vertices:
		#distancias, padre = grafo.camino_minimo(v) #con pesos
		padre, distancias = grafo.bfs(v)  #sin pesos
		
		contador_local = {}
		for vertice in distancias:
			contador_local[vertice] = 0
		
		vertices_ordenados = ordenar_vertices(grafo, distancias) #lista de tuplas, en 0 el id del vertice, en 1 la distancia
			
		for tupla in vertices_ordenados:
			if tupla[0] != v:
				contador_local[padre[tupla[0]]] += 1 + contador_local[tupla[0]]
			
		for tupla in vertices_ordenados:
			if tupla[0] != v:
				contador_apariciones_total[tupla[0]] += contador_local[tupla[0]]
	
	centrales = []
	centrales = sorted(contador_apariciones_total.items(), key=operator.itemgetter(1)) #ordeno por sumatoria total distancias
	centrales.reverse() #mayor a menor
	cont = 1 
	for tupla in centrales:
		print("central numero: " + str(cont) + " personaje: " + grafo[tupla[0]] + " sumatoria: " + str(tupla[1]))
		cont += 1
		if cont == cant_personajes:
			break
			
def distancias(grafo, origen):
	padre, distancias = grafo.bfs(origen)   #para este comando no necesito los padres pero no quise tocar el bfs para que sea mas generico
	saltos_distancias = {}
	for distancia in distancias.values():
		if distancia not in saltos_distancias:
			saltos_distancias[distancia] = 1
		else:
			saltos_distancias[distancia] += 1
	
	for distancia in saltos_distancias: #no se porque me los imprime en orden cuando es aleatorio el orden para un diccionario
		if distancia != 0:
			print("Distancia " + str(distancia) + ": " + str(saltos_distancias[distancia]))
			
	
def main():
	archivo = cargar_archivo()
	grafo, nombres = crear_grafo_y_dic_nombres(archivo)
	'''algunos comandos se pasa el nombre por parametro y en otros directamente el id, luego cuando
	hagamos la lectura por consola vamos a unificar todo'''
	#similares(grafo, nombres, "IRON MAN", 3, 50, 50)    
	#recomendar(grafo, nombres, "IRON MAN", 5, 50, 50)
	#camino(grafo, nombres["STAN LEE"], nombres["CAPTAIN AMERICA"])
	#comunidades(grafo)
	#estadisticas(grafo)
	#centralidad(grafo, 1000) #usando pesos tardo 42 minutos
	                          #sin usar pesos tardo 11 minutos
	#distancias(grafo, nombres["BLACK PANTHER"])
		
main()
