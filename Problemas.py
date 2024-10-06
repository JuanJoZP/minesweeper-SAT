from Logica import *
from itertools import combinations


def adjacent(x, y, matrix) -> list[tuple[int, int]]:
    """
    returns covered and marked boxes adjacent to (x, y).
    """
    r = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if x+i >= 0 and y+j >= 0 and x+i < len(matrix) and y+j < len(matrix):
                if matrix[x+i][y+j] in [-1, 9]: # cambiar docs, tambien incluye minas
                    r.append((x+i, y+j))
    return r


def init_MenC(descriptor, matriz): 
    """inicializa los atomos del descriptor MenC y los ubica en
    una matriz con sus coordenadas correspondientes"""
    m = [[None] * len(matriz) for i in range(len(matriz[0]))]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            casilla = matriz[i][j]
            if casilla in range(1, 9):
                close = adjacent(i, j, matriz)
                for xy in close:
                    m[xy[0]][xy[1]] = descriptor.P([xy[0], xy[1]])
            if casilla == -1: # si la casilla es mina se vuelve un átomo
                m[i][j] = descriptor.P([i, j])
    return m


def C_n(x, y, matriz, minas): # revisar que este funcionando bien
    """devuelve una lista con las posibles combinaciones
    de minas para una casilla destapada"""
    comb = []
    close = adjacent(y, x, matriz)
    minas_close = [c for c in close if matriz[c[1]][c[0]] == -1]

    casilla = matriz[y][x]
    if casilla != 0 and casilla != 9 and casilla != -1:
        #m_comb = combinations(close, casilla-len(minas_close))
        #print(casilla, "   !!!!")
        m_comb = combinations(close, casilla)

        for dist in m_comb:
            #print(dist)
            pos_comb = []
            for mina in dist:
                pos_comb.append(minas[mina[0]][mina[1]])
            for n_mina in close:
                if (n_mina not in dist):
                    pos_comb.append("-"+minas[n_mina[0]][n_mina[1]])

            #print(pos_comb)
            comb.append(pos_comb)

    return comb


class Tablero:

    '''
    Clase para representar el tablero de buscaminas, los descriptores y las reglas
    '''

    def __init__(self, length_x, width_y):
        # NOMBRES EN INGLES
        # reformat: cambiar nombre MenC por algo mas descriptivo
        # nombre funcuion regla1 -> regla
        # nombre funcion SATtabla -> solucionar o solve
        # nombre initMenC -> otra cosa
        # nombre nearby -> adjacent
        # nombre escribir_mina -> print_algo
        self.matriz = [] # ecoding: 9 -> casilla tapada, 0 -> casilla sin numero, 1 al 8: casilla con número 1 al 8, -1: bandera (mina)
        self.matriz_minas = []

        self.MenC = Descriptor([length_x, width_y])
        self.MenC.escribir = MethodType(print_bomb, self.MenC)
        self.regla = ""

    def update(self, tablero):
        self.matriz = tablero
        self.matriz_minas = init_MenC(self.MenC, self.matriz)
        self.regla = self.regla1()
        ###
        #print(inorder_to_tree(self.regla).ver(self.MenC))
        #input()
        ###

    def regla1(self):
        rule = []
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if self.matriz[i][j] in range(1,9): # esto deberia ser if casilla destapada es decir self.matriz[i][j] in range(1, 9)
                    comb = []
                    c_n = C_n(j, i, self.matriz, self.matriz_minas)  # revisar que devuelve, ver que corresponde con la regla
                    if len(c_n) != 0:
                        for pos_comb in c_n:
                            comb.append(Ytoria(pos_comb))
                        rule.append(Otoria(comb)) # revisar si realmente si es otoria y luego ytoria
                if self.matriz[i][j] == -1: # si la casilla tiene una mina entonces se añade a la regla
                    rule.append(self.matriz_minas[i][j])
                    pass
        return Ytoria(rule)

    def SATtabla(self):
        A = inorder_to_tree(self.regla)
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
