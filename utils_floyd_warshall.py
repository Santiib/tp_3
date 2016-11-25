def buscar_recorrido(origen, predecesores, destino, recorrido):

    """Reconstruye el recorrido de origen a destino, predecesores 
       es un diccionario que indica cual era el mejor paso anterior 
       para llegar desde origen a destino, recorrido una lista donde
       se almacenara el recorrido"""
   
    if destino == None:

        return recorrido[::-1]

    elif origen == destino and predecesores[origen][destino] == origen: #lazos

        recorrido.append(destino)
        return recorrido[::-1]

    recorrido.append(destino)
    return buscar_recorrido(origen, predecesores, predecesores[origen][destino], recorrido)

