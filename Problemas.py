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
        MenC_matriz = init_MenC(MenC, self.matriz)
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

    def visualizar(self, I):
        # Inicializo el plano que contiene la figura
        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        # Dibujo el tablero
        step = 1./3
        tangulos = []
        # Creo los cuadrados claros en el tablero
        tangulos.append(patches.Rectangle(
            (0, step),
            step,
            step,
            facecolor='cornsilk')
        )
        tangulos.append(patches.Rectangle(*[(step, 0), step, step],
                                          facecolor='cornsilk'))
        tangulos.append(patches.Rectangle(*[(2 * step, step), step, step],
                                          facecolor='cornsilk'))
        tangulos.append(patches.Rectangle(*[(step, 2 * step), step, step],
                                          facecolor='cornsilk'))
        # Creo los cuadrados oscuros en el tablero
        tangulos.append(patches.Rectangle(*[(2 * step, 2 * step), step, step],
                                          facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(0, 2 * step), step, step],
                                          facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(2 * step, 0), step, step],
                                          facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(step, step), step, step],
                                          facecolor='lightslategrey'))
        tangulos.append(patches.Rectangle(*[(0, 0), step, step],
                                          facecolor='lightslategrey'))
        # Creo las líneas del tablero
        for j in range(3):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.005],
                                              facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.005, 1],
                                              facecolor='black'))
        for t in tangulos:
            axes.add_patch(t)
        # Cargando imagen de caballo
        arr_img = plt.imread("./img/caballo.png", format='png')
        imagebox = OffsetImage(arr_img, zoom=0.1)
        imagebox.image.axes = axes
        # Creando las direcciones en la imagen de acuerdo a literal
        direcciones = {}
        direcciones[(0, 2)] = [0.165, 0.835]
        direcciones[(1, 2)] = [0.5, 0.835]
        direcciones[(2, 2)] = [0.835, 0.835]
        direcciones[(0, 1)] = [0.165, 0.5]
        direcciones[(1, 1)] = [0.5, 0.5]
        direcciones[(2, 1)] = [0.835, 0.5]
        direcciones[(0, 0)] = [0.165, 0.165]
        direcciones[(1, 0)] = [0.5, 0.165]
        direcciones[(2, 0)] = [0.835, 0.165]
        for l in I:
            if I[l]:
                x, y = self.CenC.inv(l)
                ab = AnnotationBbox(
                    imagebox, direcciones[(x, y)], frameon=False)
                axes.add_artist(ab)
        plt.show()


class Rejilla:

    '''
    Clase para representar el problema de poner
    un número distinto en cada una de las casillas
    de una rejilla nxn
    '''

    def __init__(self, N=2, M=2):
        self.N = N
        self.M = M
        self.NenC = Descriptor([N*M, N, M])
        self.NenC.escribir = MethodType(escribir_rejilla, self.NenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3]

    def regla1(self):
        casillas_num = [(n, x, y) for n in range(self.N*self.M)
                        for x in range(self.N) for y in range(self.M)]
        lista = []
        for c in casillas_num:
            n, x, y = c
            otras_casillas = [(x1, y1) for x1 in range(self.N)
                              for y1 in range(self.M) if (x1, y1) != (x, y)]
            lista_o = []
            for k in otras_casillas:
                lista_o.append(self.NenC.P([n, *k]))
            form = '(' + self.NenC.P([*c]) + '>-' + Otoria(lista_o)
            lista.append(form)
        return Ytoria(lista)

    def regla2(self):
        casillas_num = [(n, x, y) for n in range(self.N*self.M)
                        for x in range(self.N) for y in range(self.M)]
        lista = []
        for c in casillas_num:
            n, x, y = c
            otros_numeros = [k for k in range(self.N*self.M) if k != n]
            lista_o = []
            for k in otros_numeros:
                lista_o.append(self.NenC.P([k, x, y]))
            form = '(' + self.NenC.P([*c]) + '>-' + Otoria(lista_o) + ')'
            lista.append(form)
        return Ytoria(lista)

    def regla3(self):
        casillas = [(x, y) for x in range(self.N) for y in range(self.M)]
        lista = []
        for c in casillas:
            lista_o = []
            for n in range(self.N*self.M):
                lista_o.append(self.NenC.P([n, *c]))
            lista.append(Ytoria(lista_o))
        return Ytoria(lista)

    def visualizar(self, I):
        fig, axes = plt.subplots()
        fig.set_size_inches(self.N, self.M)
        step_x = 1. / self.N
        step_y = 1. / self.M
        offset = 0.001
        tangulos = []
        tangulos.append(patches.Rectangle((0, 0), 1, 1,
                                          facecolor='cornsilk', edgecolor='black', linewidth=2))
        u = self.N // 2 if self.N % 2 == 0 else self.N // 2 + 1  # Filas par o impar
        v = self.M // 2 if self.M % 2 == 0 else self.M // 2 + 1  # Columnas par o impar
        for i in range(u + 1):
            for j in range(v):
                tangulos.append(patches.Rectangle((2 * i * step_x, 2 * j * step_y),
                                                  step_x - offset, step_y,
                                                  facecolor='lightslategrey',
                                                  ec='k', lw=3))
                tangulos.append(patches.Rectangle((step_x + 2 * i * step_x, (2 * j + 1) * step_y),
                                                  step_x - offset, step_y,
                                                  facecolor='lightslategrey',
                                                  ec='k', lw=3))
        for t in tangulos:
            axes.add_patch(t)
        offsetX = 0.065
        offsetY = 0.065
        for k in I:
            n, X, Y = self.NenC.inv(k)
            if I[k]:
                axes.text(X * step_x + step_x / 2, Y * step_y + step_y / 2, n,
                          ha="center", va="center", size=30, c='k')
        axes.axis('off')
        plt.show
