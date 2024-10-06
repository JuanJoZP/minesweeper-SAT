from minesweeper import Minesweeper
from minesweeper import inorder_to_tree

matriz_inicial= [
    [0, 0, 1, 9, 9, 9, 9, 9],
    [0, 0, 1, 9, 9, 9, 9, 9],
    [0, 0, 1, 3, 9, 9, 9, 9],
    [1, 1, 0, 1, 9, 9, 9, 9],
    [9, 1, 1, 2, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9]
    ]  

matriz_2= [
    [0, 0, 1, 3, 9, 9, 9, 9],
    [0, 0, 1, -1, 9, 9, 9, 9],
    [0, 0, 1, 3, 9, 9, 9, 9],
    [1, 1, 0, 1, 9, 9, 9, 9],
    [-1, 1, 1, 2, 2, 9, 9, 9],
    [1, 2, 2, -1, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9],
    ]  

tab = Minesweeper(9, 9)
tab.update(matriz_2)
for interpretacion in tab.solve():
   print(interpretacion)

#print(inorder_to_tree(tab.regla))

for (i, row) in enumerate(tab.bomb_matrix):
    for (j, c) in enumerate(row):
        if c == None:
            row[j] = tab.board_matrix[i][j]
    frmt = "{:>3}"*len(row)
    print(frmt.format(*row))