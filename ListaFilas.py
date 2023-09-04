import os
import re
import pandas as pd
from dotenv import load_dotenv

import Lista
from Fila import Fila
from Frutas import Frutas

class ListaFilas(Lista.Lista):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self._frutas = Frutas()


    def getFrutas(self):
        return self._frutas
    

    def setFrutas(self, frutas):
        self._frutas = frutas

    def xlsxToObject(self, df):
        for index, row in df.iterrows():
            fila = []
            # Accede a los valores de cada columna en la fila actual
            for columna in df.columns:
                fila.append(row[f'{columna}'])
            if(
                not pd.isna(fila[0]) and fila[0] != os.environ.get('LAYOUT_TOTAL') 
                and not os.environ.get('LAYOUT_LEGEND_ES') in fila[0]
                and not os.environ.get('LAYOUT_LEGEND_EN') in fila[0]
                ):
                self._elementos.append(Fila(*fila))
        self.sorted()


    def recuperaFila(self, oc, articulo):
        for fila in self._elementos:
            if (fila.getSerieLote() == oc and fila.getArticulo() == articulo):
                return fila
        return None


    # def mensajeSeparado(self):
    #     titulos = []
    #     string = ''
    #     for fila in self._elementos:
    #         if(not titulos):
    #             titulos.append(fila.titulo())
    #             string = f'{fila.titulo()}'
    #             string = f'{string}\n{fila.detalles()}'
    #         else:
    #             if (not fila.titulo() in titulos):
    #                 titulos.append(fila.titulo())
    #                 string = f'{string}\n\n{fila.titulo()}'
    #                 string = f'{string}\n{fila.detalles()}'
    #             else:
    #                 string = f'{string}\n{fila.detalles()}'
    #     return string

    def returnShortCode(self, key):
        splitKey = key.split(':')[1]
        return self._frutas.__dict__.get(f'{splitKey}', "")


    def titulos(self):
        titulos = {}
        especies = []
        emojis = []
        keys = []
        etiquetas = []
        validando = ''
        for fila in self._elementos:
            if (validando == ''):
                validando = fila.getSerieLote()

            if (fila.getSerieLote() == validando):
                emoji = self.returnShortCode(fila.getEmoji())
                if (not fila.getEspecie() in especies):
                    especies.append(fila.getEspecie())
                if (not emoji in emojis):
                    emojis.append(emoji)
                    keys.append(fila.getEmoji())
                if (not fila.getEtiqueta() in etiquetas):
                    etiquetas.append(fila.getEtiqueta())

            else:
                titulos[f'{validando}'] = f'*{validando[:-1]} {"/".join(str(especie) for especie in especies)} {" ".join(str(key) for key in keys)} {"/".join(etiqueta for etiqueta in etiquetas)}*'
                validando = fila.getSerieLote()
                especies = []
                emojis = []
                keys = []
                etiquetas = []
                emoji = self.returnShortCode(fila.getEmoji())
                especies.append(fila.getEspecie())
                emojis.append(emoji)
                keys.append(fila.getEmoji())
                etiquetas.append(fila.getEtiqueta())

            titulos[f'{validando}'] = f'*{validando[:-1]} {"/".join(str(especie) for especie in especies)} {" ".join(str(key) for key in keys)} {"/".join(etiqueta for etiqueta in etiquetas)}*'
        return titulos


    def mensaje(self):
        titulosEnUso = []
        titulos = self.titulos()
        mensaje = ''
        for fila in self._elementos:
            if (not titulos[fila.getSerieLote()] in titulosEnUso):
                if (mensaje == ''):
                    mensaje = f'{titulos[fila.getSerieLote()]}'
                else:
                    mensaje = f'{mensaje}\n\n{titulos[fila.getSerieLote()]}'
                mensaje = f'{mensaje}\n{fila.detalles()}'
                titulosEnUso.append(titulos[fila.getSerieLote()])
            else:
                mensaje = f'{mensaje}\n{fila.detalles()}'
        return mensaje


    def extraerClave(self, elemento):
        prefijo, numero = elemento.getSerieLote().split(' ')
        numero = int(re.search(r'\d+', numero).group())
        return (prefijo, int(numero))


    def sorted(self):
        self._elementos = sorted(self._elementos, key=self.extraerClave)


    def viewJsonElements(self):
        for fila in self._elementos:
            print(fila.titulo())
            print(fila.detalles())
            print(fila.objectToJson())


    def _logError(self, metodo, error):
        print(f'{self._tiempo} || ListaFilas in {metodo}: {error}')