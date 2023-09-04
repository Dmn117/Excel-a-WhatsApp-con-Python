import datetime


class Lista:
    def __init__(self):
        self._elementos = []
        self._tuplas = []
        self._tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



    def getElementos(self, indice = None):
        if(indice == None):
            return self._elementos
        else:
            return self._elementos[indice]
        

    def getTuplas(self, indice = None):
        if (indice):
            return self._tuplas[indice]
        else:
            return self._tuplas


    def setElementos(self, elementos):
        self._elementos = elementos

    
    def setTuplas(self, tuplas):
        self._tuplas = tuplas


    def append(self, elemento):
        self._elementos.append(elemento)


    def objectToTuple(self):
        self._tuplas = [
            objeto.objectToTuple()
            for objeto in self._elementos
        ]
        return self._tuplas
    

    #---------------------------------------------Funcion para Imprimir Errores
    def _logError(self, metodo, error):
        print(f'{self._tiempo} || Lista in {metodo}: {error}')