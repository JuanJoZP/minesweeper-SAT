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
    r = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x+i >= 0 and y+j >= 0 and x+i < len(matriz) and y+j < len(matriz):
                if matriz[x+i][y+j] == 9:
                    r.append((x+i, y+j))
    return r


def init_MenC(descriptor, matriz):
    m = np.zeros((len(matriz), len(matriz[0])), dtype=int)
    for i in range(matriz):
        for j in range(matriz[i]):
            casilla = matriz[i][j]
            if casilla != 0 and casilla != 9:
                # si las casillas aledañas son 9 crea el descriptor
                close = closeBy(i, j, matriz)
                for xy in close:
                    m[xy[0], xy[1]] = descriptor.P([xy[0], xy[1]])


class Tablero:

    '''
    Clase para representar el problema de poner
    tres caballos en un tablero de ajedrez sin que se
    puedan atacar el uno al otro.
    '''

    def __init__(self):
        self.matriz = [
            [0, 0, 0, 1, 9, 9, 9, 9], [0, 0, 1, 2, 9, 9, 9, 9],
            [0, 1, 2, 9, 9, 9, 9, 9], [0, 1, 9, 9, 9, 9, 9, 9],
            [0, 1, 1, 3, 9, 9, 9, 9], [0, 0, 0, 2, 9, 9, 9, 9],
            [1, 2, 1, 2, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9]
        ]

        self.MenC = Descriptor([8, 8])
        #self.CenC.escribir = MethodType(escribir_caballos, self.CenC)
        MenC_matriz = init_MenC(self.MenC, self.matriz)
        for row in MenC_matriz:
            for d in row:
                print(d)
        r1 = self.regla1()

    def regla1(self):
        casillas = [(x, y) for x in range(3) for y in range(3)]
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
        return Otoria(lista)

    def regla2(self):
        tripletas = [((0, 0), (1, 2), (2, 1)),
                     ((1, 0), (0, 2), (2, 2)),
                     ((2, 0), (1, 2), (0, 1)),
                     ((0, 1), (2, 2), (2, 0)),
                     ((2, 1), (0, 2), (0, 0)),
                     ((0, 2), (1, 0), (2, 1)),
                     ((1, 2), (0, 0), (2, 0)),
                     ((2, 2), (0, 1), (1, 0)),
                     ]
        lista = []
        for t in tripletas:
            c1, c2, c3 = t
            f = '(' + self.CenC.P([*c1]) + '>-(' + \
                self.CenC.P([*c2]) + 'O' + self.CenC.P([*c3]) + '))'
            lista.append(f)
        return Ytoria(lista)

    def regla3(self):
        return self.CenC.P([1, 2])
