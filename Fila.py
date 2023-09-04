import json

class Fila:
    def __init__(self, especie='', variedad='', etiqueta='', calidad='',
                calibre='', empaque='', presentacion='', serieLote='',
                diasEntrada='', articulo='', mayoreo='', transito='', 
                costeo='', gdl='', mex='', mxl='', estatus=''):
        self._especie = especie
        self._variedad = variedad
        self._etiqueta = etiqueta
        self._calidad = calidad
        try:
            float(calibre)
            self._calibre = f'{format(calibre, ".0f")}'
        except ValueError:
            self._calibre = calibre
        # self._calibre = calibre
        # print(calibre)
        # if (calibre.isdigit()):
        #     print(calibre)
        #     self._calibre = int(calibre)
        # else:
        #     self._calibre = calibre
        self._empaque = empaque
        self._presentacion = presentacion
        self._articulo = articulo
        self._serieLote = serieLote
        self._diasEntrada = diasEntrada
        self._mayoreo = float(mayoreo)
        self._menudeo = float(mayoreo) + 20
        self._transito = transito
        self._costeo = costeo
        self._gdl = gdl
        self._mex = mex
        self._mxl = mxl
        self._estatus = estatus
        self._emoji = f':{self._especie.lower()} {self._variedad.lower()}:'


    def getEspecie(self):
        return self._especie

    def getVariedad(self):
        return self._variedad

    def getEtiqueta(self):
        return self._etiqueta

    def getCalidad(self):
        return self._calidad

    def getCalibre(self):
        return self._calibre

    def getEmpaque(self):
        return self._empaque

    def getPresentacion(self):
        return self._presentacion
    
    def getSerieLote(self):
        return self._serieLote
    
    def getDiasEntrada(self):
        return self._diasEntrada

    def getArticulo(self):
        return self._articulo

    def getMayoreo(self):
        return self._mayoreo

    def getMenudeo(self):
        return self._menudeo

    def getTransito(self):
        return self._transito

    def getCosteo(self):
        return self._costeo

    def getGdl(self):
        return self._gdl

    def getMex(self):
        return self._mex

    def getMxl(self):
        return self._mxl

    def getEstatus(self):
        return self._estatus

    def getEmoji(self):
        return self._emoji


    def setEspecie(self, especie):
        self._especie = especie

    def setVariedad(self, variedad):
        self._variedad = variedad

    def setEtiqueta(self, etiqueta):
        self._etiqueta = etiqueta

    def setCalidad(self, calidad):
        self._calidad = calidad

    def setCalibre(self, calibre):
        self._calibre = calibre

    def setEmpaque(self, empaque):
        self._empaque = empaque

    def setPresentacion(self, presentacion):
        self._presentacion = presentacion

    def setSerieLote(self, serieLote):
        self._serieLote = serieLote

    def setDiasEntrada(self, diasEntrada):
        self._diasEntrada = diasEntrada

    def setArticulo(self, articulo):
        self._articulo = articulo

    def setMayoreo(self, mayoreo):
        self._mayoreo = float(mayoreo)

    def setMenudeo(self, menudeo):
        self._menudeo = float(menudeo)

    def setTransito(self, transito):
        self._transito = transito

    def setCosteo(self, costeo):
        self._costeo = costeo

    def setGdl(self, gdl):
        self._gdl = gdl

    def setMex(self, mex):
        self._mex = mex

    def setMxl(self, mxl):
        self._mxl = mxl

    def setEstatus(self, estatus):
        self._estatus = estatus

    def setEmoji(self, emoji):
        self._emoji = emoji


    def objectToJson(self):
        return json.dumps(self.__dict__, indent=4)


    def titulo(self):
        return f'*{self._serieLote[:-1]} {self._especie} {self._emoji} {self._variedad} {self._etiqueta}*'


    def detalles(self):
        return f'{self._transito}cjs - *{self._calibre}* {self._calidad} {self._variedad} ${format(self._mayoreo, ".0f")}'
