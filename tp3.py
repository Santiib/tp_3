# -*- coding: utf-8 -*-
from grafo import *
import sys
import operator
import random
'''import collections
from print_test import *'''

def cargar_archivo():
	#print ('Argument List:', str(sys.argv))
	try:
		#archivo = open((sys.argv),'r')
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
	nombres = {}
	
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

def random_walk(grafo, nombres, origen, caminos, largo, pesado = True): #creo que caminos y largo conviene definirlo al principio del archivo, y si es pesado o no ponerlo en el init del grafo.
	caminos_hechos = 0
	largo_actual = 0
	similitudes = {}
	actual = nombres[origen]
	while caminos_hechos < caminos:		
		while largo_actual < largo:
			posibles = []
			for v in grafo.vertices[actual][1]:
				posibilidades = 1
				if pesado:
					posibilidades = grafo.vertices[actual][1][v] #peso
				for i in range(0,posibilidades):
					posibles.append(v)
			nuevo = posibles[random.randrange(len(posibles))]
			if nuevo in similitudes:
				similitudes[nuevo] +=1
			else:
				similitudes[nuevo] = 1
			actual = nuevo
			largo_actual += 1
		
		actual = nombres[origen]
		largo_actual = 0
		caminos_hechos += 1
	return similitudes	

def similares(grafo, nombres, vertice, cantidad, caminos, largo, pesado = True): #esta hecho teniendo en cuenta que vertice es el id y no el nombre/valor.
	similitudes = random_walk(grafo, nombres, vertice, caminos, largo, pesado)
	similitudes_lista = sorted(similitudes.items(), key=operator.itemgetter(1)) #ordena de menor a mayor por similitud
	mas_similares = []
	a_imprimir = 0
	for v in similitudes_lista[::-1]:
		if v[0] == nombres[vertice]:
			continue
		if a_imprimir == cantidad:
			break
		mas_similares.append(grafo.vertices[v[0]][0])
		a_imprimir += 1
	print (', '.join(mas_similares))
	
def recomendar(grafo, nombres, vertice, cantidad, caminos, largo, pesado = True): #esta hecho teniendo en cuenta que vertice es el id y no el nombre/valor.
	similitudes = random_walk(grafo, nombres, vertice, caminos, largo, pesado)
	similitudes_lista = sorted(similitudes.items(), key=operator.itemgetter(1)) #ordena de menor a mayor por similitud
	recomendaciones = []
	agregados = 0
	for v in similitudes_lista[::-1]:
		if v[0] == nombres[vertice]:
			continue
		if agregados == cantidad:
			break
		if v[0] not in grafo.vertices[nombres[vertice]][1]:
			recomendaciones.append(grafo.vertices[v[0]][0])
			agregados += 1
	print (', '.join(recomendaciones)	)

#def camino(grafo, nombres, vertice, caminos, , pesado = False):
	
def main():
	archivo = cargar_archivo()
	grafo, nombres = crear_grafo_y_dic_nombres(archivo)
	#similitudes = random_walk(grafo, nombres, "PUCK", 10, 10)
	#print similitudes
	#similares(grafo, nombres, "PUCK", 4, 50, 50)
	#recomendar(grafo, nombres, "PUCK", 2, 50, 50)
	'''camino = grafo.camino_minimo(nombres["STAN LEE"],nombres["CAPTAIN AMERICA"], True)
	nombres_camino = []
	for id in camino:
		nombres_camino.append(grafo[id] + " ->")
	
	print(nombres_camino)'''
	
main()

