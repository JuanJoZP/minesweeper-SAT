from itertools import combinations
from Logica import *
from types import MethodType
import numpy as np

'''
def escribir_caballos(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    x, y  = self.inv(atomo)
    return f"El caballo{neg} está en la casilla ({x},{y})"

def escribir_rejilla(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    n, x, y  = self.inv(atomo)
    return f"El número {n}{neg} está en la casilla ({x},{y})"
'''


def closeBy(x, y, matriz):
    """devuelve las casillas tapadas aledañas a (x, y)"""
    r = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x+i >= 0 and y+j >= 0 and x+i < len(matriz) and y+j < len(matriz):
                if matriz[x+i][y+j] == 9:
                    r.append((x+i, y+j))
    return r


def init_MenC(descriptor, matriz):
    """inicializa los atomos del descriptor MenC y los ubica en
    una matriz con sus coordenadas correspondientes"""
    m = [[None] * len(matriz) for i in range(len(matriz[0]))]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            casilla = matriz[i][j]
            if casilla != 0 and casilla != 9:
                close = closeBy(i, j, matriz)
                for xy in close:
                    m[xy[0]][xy[1]] = descriptor.P([xy[0], xy[1]])
    return m


class Tablero:

    '''
    Clase para representar el tablero de buscaminas, los descriptores y las reglas
    '''

    def __init__(self, width_x, width_y, tablero):
        self.matriz = tablero

        self.MenC = Descriptor([width_x, width_y])
        #self.CenC.escribir = MethodType(escribir_caballos, self.CenC)
        MenC_matriz = init_MenC(self.MenC, self.matriz)
        for row in MenC_matriz:
            print(row)
        r1 = self.regla1()

    def regla1(self):
        """casillas = [(x, y) for x in range(3) for y in range(3)]
        tripletas = list(combinations(casillas, 3))
        lista = []
        for t in tripletas:
            c1, c2, c3 = t
            f = '((' + self.CenC.P([*c1]) + 'Y' + \
                self.CenC.P([*c2]) + ')Y' + self.CenC.P([*c3]) + ')'
            otras_casillas = [c for c in casillas if c not in t]
            lista_negs = ['-' + self.CenC.P([*c]) for c in otras_casillas]
            f = '(' + f + 'Y' + Ytoria(lista_negs) + ')'
            lista.append(f)
        return Otoria(lista)"""


matriz = [
    [0, 0, 0, 1, 9, 9, 9, 9], [0, 0, 1, 2, 9, 9, 9, 9],
    [0, 1, 2, 9, 9, 9, 9, 9], [0, 1, 9, 9, 9, 9, 9, 9],
    [0, 1, 1, 3, 9, 9, 9, 9], [0, 0, 0, 2, 9, 9, 9, 9],
    [1, 2, 1, 2, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9]
]
tablero = Tablero(8, 8, matriz)
