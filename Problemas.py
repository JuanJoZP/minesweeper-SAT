from Logica import *
from types import MethodType
from itertools import combinations

"""
def SATtabla(A):
    letras = A.letras()
    inter_a = list(product(*[[True, False] for i in letras]))
    I_map = []
    solutions = []
    for i in inter_a:
        I_temp = {}
        j_index = 0
        for j in letras:
            I_temp[j] = i[j_index]
            j_index += 1
        I_map.append(I_temp)

    for i in I_map:
        if A.valor(i):
            solutions.append(i)
    return solutions
"""


def escribir_mina(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    x, y = self.inv(atomo)
    return f"{neg} hay una mina en la casilla ({x},{y})"


def nearby(x, y, matriz):
    """devuelve las casillas tapadas aledañas a (x, y).
       devuelve una lista de tuplas con el formato (a, b)
    """
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
                close = nearby(i, j, matriz)
                for xy in close:
                    m[xy[0]][xy[1]] = descriptor.P([xy[0], xy[1]])
    return m


def C_n(x, y, matriz, minas):
    """devuelve una lista con las posibles combinaciones
    de minas para una casilla destapada"""
    comb = []
    close = nearby(y, x, matriz)
    casilla = matriz[y][x]
    if casilla != 0 and casilla != 9:
        m_comb = combinations(close, casilla)

        for dist in m_comb:
            pos_comb = []
            for mina in dist:
                pos_comb.append(minas[mina[0]][mina[1]])
            for n_mina in close:
                if (n_mina not in dist):
                    pos_comb.append("-"+minas[n_mina[0]][n_mina[1]])

            comb.append(pos_comb)

    return comb


class Tablero:

    '''
    Clase para representar el tablero de buscaminas, los descriptores y las reglas
    '''

    def __init__(self, length_x, width_y, tablero):
        self.matriz = tablero

        self.MenC = Descriptor([length_x, width_y])
        self.MenC.escribir = MethodType(escribir_mina, self.MenC)
        self.matriz_minas = init_MenC(self.MenC, self.matriz)
        self.regla = self.regla1()

    def regla1(self):
        rule = []
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if self.matriz[i][j] != 0 and self.matriz[i][j] != 9:
                    comb = []
                    for pos_comb in C_n(j, i, self.matriz, self.matriz_minas):
                        comb.append(Ytoria(pos_comb))
                    rule.append(Otoria(comb))
        return Ytoria(rule)
