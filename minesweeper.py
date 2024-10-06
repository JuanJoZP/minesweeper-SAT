from logica import *
import itertools

class Minesweeper:
    def __init__(self, length_x, width_y):
        self.board_matrix = [] # ecoding: 9 -> casilla tapada, 0 -> casilla sin numero, 1 al 8: casilla con número 1 al 8, -1: bandera (mina)
        self.bomb_matrix = []
        self.bomb_in_box = Descriptor([length_x, width_y])
        self.rule = ""

    def update(self, new_board):
        self.board_matrix = new_board
        self.bomb_matrix = self.initial_bomb_matrix()
        self.rule = self.generate_rule()

    def solve(self) -> list[dict[str, bool]]:
        """checks the complete truth table and returns a list with all the satisfiable interpretations. An interpretation is of the form {"atom1": True, "atom2": False, ...}"""
        formula = inorder_to_tree(self.rule)
        literals = formula.letras()
        interpretations_a = list(product(*[[True, False] for i in literals]))
        I_map = []
        solutions = []

        for i in interpretations_a:
            I_temp = {}
            j_index = 0
            for j in literals:
                I_temp[j] = i[j_index]
                j_index += 1
            I_map.append(I_temp)

        for i in I_map:
            # if interpretation satisfies formula, add it to solutions
            if formula.valor(i): 
                solutions.append(i)

        return solutions
    
    def initial_bomb_matrix(self): 
        """inits atoms "bomb in box" and places them into a matrix"""
        bombs = [[None] * len(self.board_matrix) for i in range(len(self.board_matrix[0]))]
        for i in range(len(self.board_matrix)):
            for j in range(len(self.board_matrix[i])):
                box = self.board_matrix[i][j]
                if box in range(1, 9): # if box is uncovered, creates atoms for all its adjacent cells
                    close = self.adjacent(i, j)
                    for xy in close:
                        bombs[xy[0]][xy[1]] = self.bomb_in_box.P([xy[0], xy[1]])
                if box == -1: # if box is a bomb, creates atom for itself
                    bombs[i][j] = self.bomb_in_box.P([i, j])
        return bombs
    
    def generate_rule(self):
        rules = []
        for i in range(len(self.board_matrix)):
            for j in range(len(self.board_matrix[0])):
                # if box is uncovered adds possible bombs combinations to the rule
                if self.board_matrix[i][j] in range(1,9): 
                    posible_combinations = []
                    atoms_combinations = self.atoms_combinations(j, i)  
                    if len(atoms_combinations) != 0:
                        for atoms_combination in atoms_combinations: # atoms is list of atoms describing one possible combination
                            posible_combinations.append(Ytoria(atoms_combination))
                        rules.append(Otoria(posible_combinations))
                # if box is already marked as a bomb, add to the rule, the atom representing that bomb
                if self.board_matrix[i][j] == -1: 
                    rules.append(self.bomb_matrix[i][j])
        return Ytoria(rules)

    def atoms_combinations(self, x, y):
        """for box in coordinate (x, y) returns a list with all possible combinations for its adjacent atoms"""
        combination = []
        adjacent_boxes = self.adjacent(y, x)
        box = self.board_matrix[y][x]

        if box in range(1, 9):
            bombs_combinations = itertools.combinations(adjacent_boxes, box)

            for distribution in bombs_combinations:
                possible_combination = []
                # adds boxes in distribution to the combination as "bomb"
                for bomb in distribution:
                    possible_combination.append(self.bomb_matrix[bomb[0]][bomb[1]])
                for adjacent in adjacent_boxes:
                    # adds the remaining boxes to the combination as "no bomb"
                    if (adjacent not in distribution):
                        possible_combination.append("-"+self.bomb_matrix[adjacent[0]][adjacent[1]])

                combination.append(possible_combination)

        return combination
    
    def adjacent(self, x, y) -> list[tuple[int, int]]:
        """returns covered and marked boxes adjacent to (x, y)"""
        r = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if x+i >= 0 and y+j >= 0 and x+i < len(self.board_matrix) and y+j < len(self.board_matrix):
                    if self.board_matrix[x+i][y+j] in [-1, 9]: 
                        r.append((x+i, y+j))
        return r


    





