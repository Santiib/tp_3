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
		raise IOError("no se reconocio")
		
def crear_grafo(archivo):
	primer_linea = archivo.readline()
	
	palabras = []
	palabras = primer_linea.split(" ")
	
	cant_vertices = int(palabras[1])
	
	grafo = Grafo()
	
	for pos in range(0, cant_vertices):
		#print(pos)
		linea = archivo.readline()
		palabras = linea.split(" ")
		id = int(palabras.pop(0))
		nombre_personaje = ' '.join(palabras)
		nombre_personaje = nombre_personaje[1:-2] #saco comillas
		grafo[id] = nombre_personaje
		
	linea = archivo.readline()
	linea = archivo.readline()
	
	while(linea):
		#print(linea)
		palabras = linea.split(" ")
		vertice_origen = int(palabras[0])
		vertice_destino = int(palabras[1])
		peso = int(palabras[2])
		grafo.agregar_arista(vertice_origen, vertice_destino, peso)
		linea = archivo.readline()
	
	print("holaaaaaa")
	archivo.close()
	return grafo
	

def random_walk(grafo, origen, caminos, largo, pesado = True): #creo que caminos y largo conviene definirlo al principio del archivo, y si es pesado o no ponerlo en el init del grafo.
	caminos_hechos = 0
	largo_actual = 0
	similitudes = {}
	actual = origen
	#print grafo.vertices[actual][0]
	while caminos_hechos < caminos:
		
		while largo_actual < largo:
			adyacentes = []
			nuevo = False
			for v in grafo.vertices[actual][1]:
				posibilidades = 1
				if pesado:
					posibilidades = grafo.vertices[actual][1][v] #peso
				for i in range(0, posibilidades):
					if random.randrange(4) == 1: #25% posibilidades
						nuevo = True
						break
				if nuevo:
					break
			if v in similitudes:
				similitudes[v] +=1
			else:
				similitudes[v] = 1
			actual = v
			largo_actual += 1
		
		actual = origen
		largo_actual = 0
		caminos_hechos += 1
	return similitudes	

def similares(grafo, vertice, cantidad, caminos, largo, pesado = True): #esta hecho teniendo en cuenta que vertice es el id y no el nombre/valor.
	similitudes = random_walk(grafo, vertice, caminos, largo, pesado)
	similitudes_lista = sorted(similitudes.items(), key=operator.itemgetter(1)) #ordena de menor a mayor por similitud
	mas_similares = []
	a_imprimir = 0
	for v in similitudes_lista[::-1]:
		if v[0] == vertice:
			continue
		if a_imprimir == cantidad:
			break
		mas_similares.append(grafo.vertices[v[0]][0])
		a_imprimir += 1
	print ', '.join(mas_similares)
	
def recomendar(grafo, vertice, cantidad, caminos, largo, pesado = True): #esta hecho teniendo en cuenta que vertice es el id y no el nombre/valor.
	similitudes = random_walk(grafo, vertice, caminos, largo, pesado)
	similitudes_lista = sorted(similitudes.items(), key=operator.itemgetter(1)) #ordena de menor a mayor por similitud
	recomendaciones = []
	agregados = 0
	for v in similitudes_lista[::-1]:
		if v[0] == vertice:
			continue
		if agregados == cantidad:
			break
		if v[0] not in grafo.vertices[vertice][1]:
			recomendaciones.append(grafo.vertices[v[0]][0])
			agregados += 1
	print ', '.join(recomendaciones)	

def main():
	archivo = cargar_archivo()
	grafo = crear_grafo(archivo)
	similitudes = random_walk(grafo, 2, 10, 10)
	#print similitudes
	similares(grafo, 2, 4, 10, 10)
	recomendar(grafo,2, 2, 10, 10)
	
main()

