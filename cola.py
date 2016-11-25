class _Nodo(object):

    def __init__(self, dato = None, prox = None):
        self.dato = dato
        self.prox = prox

    def __str__(self):
        return str(self.dato)

class ColaVacia(Exception):
    pass

class Cola(object): #Queue

    def __init__(self):
        self.primero = None
        self.ultimo = None

    def encolar(self, dato): #enqueue
        nodo = _Nodo(dato)
        if not self.primero:
            self.primero = nodo            
        else:
            self.ultimo.prox = nodo

        self.ultimo = nodo

    def desencolar(self):
        if not self.primero:
            raise ColaVacia()
        primero = self.primero
        self.primero = self.primero.prox
        return primero.dato

    def ver_primero(self):
        if not self.primero:
            raise ColaVacia()
        return self.primero.dato

    def esta_vacia(self):
        return not self.primero

