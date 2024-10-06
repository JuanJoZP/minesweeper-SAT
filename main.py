import subprocess
import time
import os
import argparse
from game import Game
from solver import Solver


class ConsoleApp:

    def __init__(self, difficulty, auto=False):
        size_map = {'1': 5, '2': 8, '3': 12}
        mines_map = {'1': 3, '2': 10, '3': 35}

        self.sleep = 0 if auto else 1
        self.size = size_map[difficulty]
        self.mines = mines_map[difficulty]
        self.flagged = []
        self.solver = Solver(int(size_map[difficulty]))
        self.game_process = subprocess.Popen(
            ['python', 'game.py', '--size',
             str(self.size), '--mines',
             str(self.mines)],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # get initial stdout
        self.clear_console()
        self.board = self.get_board()
        self.solver.update(self.board)
        print("Let's uncover (0, 0)!")
        time.sleep(1.5)
        self.clear_console()
        # uncover first box
        self.game_process.stdin.write("r 0 0\n".encode("utf-8"))
        self.game_process.stdin.flush()

        # FALTA MANEJAR SI SE ESTALLO A LA PRIMERA
        self.board = self.get_board()
        self.solver.update(self.board)
        self.actions_cycle(auto)

    def actions_cycle(self, auto):
        while True:
            print("Calculating...")
            time.sleep(self.sleep)
            [actions, probabilities_info] = self.get_actions()
            if len(actions) > 0:
                self.execute_actions(actions)
            else:
                if not auto:
                    print(
                        "The algorith is not sure... but it calculated the probabilities of a bomb in each box."
                    )
                    for (i, (box, probability)) in enumerate(probabilities_info.items()):
                        print(f"Option {i+1}. " + str(box) + " -> " +
                              str(round(probability * 100, 2)) + "%")
                    chosen = input("You have to choose one option to reveal: ")
                    coords = list(probabilities_info.keys())[int(chosen) - 1]
                    action = f'r {coords[0]} {coords[1]}\n'
                    self.execute_actions([action])
                else:
                    min = 1
                    arg_min = None
                    for box, probability in probabilities_info.items():
                        if probability < min:
                            arg_min = box
                    action = f'r {arg_min[0]} {arg_min[1]}\n'
                    self.execute_actions([action])

    def get_board(self):
        """reads stdout end extracts the board, then print stdout."""
        output = self.game_process.stdout.read1().decode("utf-8")
        print(output)
        return self.stdout_to_board(output)

    def stdout_to_board(self, output: str) -> list[list[int]]:
        try:
            rows = output.split("\n")[-self.size - 1:-1]
            board = []
            for row in rows:
                new_row = []
                for box in row.split(" "):
                    if box == "-":
                        new_row.append(9)
                    elif box == "X":
                        new_row.append(-1)
                    elif int(box) in range(0, 9):
                        new_row.append(int(box))

                board.append(new_row)

            return board
        except ValueError as err:
            if box == "M" or box == "Congratulations!":
                exit()  # it means that game is over
            else:
                raise Exception("parsing outside of the board") from err

    # only for debug purposes
    def print_board(self, board: list[list[int]]):
        for row in board:
            frmt = "{:>3}" * len(row)
            print(frmt.format(*row))

    def get_actions(self):
        interpretations = self.solver.solve()
        probabilities = self.get_atoms_probabilities(interpretations)
        actions = []
        probabilities_info = {}
        for atom, probability in probabilities.items():
            coords = self.solver.bomb_in_box.inv(atom)
            y = int(coords[0])
            x = int(coords[1])

            if probability == 1:
                if (x, y) not in self.flagged:
                    self.flagged.append((x, y))
                    actions.append(f"f {y} {x}\n")
            elif probability == 0:
                actions.append(f"r {y} {x}\n")
            else:
                probabilities_info[(y, x)] = probability

        return [actions, probabilities_info]

    def get_atoms_probabilities(self,
                                interpretations: list[dict[str, bool]]) -> dict[str, int]:
        atom_counts = {}
        for atom in interpretations[0]:
            atom_counts[atom] = 0

        for interpretation in interpretations:
            for atom in interpretation:
                if interpretation[atom]:
                    atom_counts[atom] += 1

        atom_probabilities = {}
        for atom in atom_counts:
            atom_probabilities[atom] = atom_counts[atom] / len(interpretations)
        return atom_probabilities

    def execute_actions(self, actions: list[str]):
        print("Executing actions!")
        for action in actions:
            print(action)
            time.sleep(self.sleep)
            self.clear_console()
            self.game_process.stdin.write(action.encode("utf-8"))
            self.game_process.stdin.flush()
            self.board = self.get_board()

        self.solver.update(self.board)

    def clear_console(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically solve Minesweeper!")
    parser.add_argument('--auto', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    print("=" * 70)
    print(" " * 10 + "🚩 Welcome to the Minesweeper Automatic Solver! 🚩")
    print("=" * 70)
    print()
    print("This program solves the classic Minesweeper game by translating it into")
    print("a SAT (Satisfiability) problem, ensuring logical and efficient solutions.")
    print()
    print("Please choose your difficulty level:")
    print("1. Beginner 🟢")
    print("2. Intermediate 🟡")
    print("3. Expert 🔴")
    print()
    while True:
        difficulty = input(
            "Enter your choice (1 for Easy, 2 for Medium, 3 for Difficult): ")
        if difficulty in ['1', '2', '3']:
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

    difficulty_map = {'1': 'Beginner 🟢', '2': 'Intermediate 🟡', '3': 'Expert 🔴'}
    print(f"\nYou selected: {difficulty_map[difficulty]}")
    print("\nThe game is about to start...")
    for i in range(3, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n💥 Boom! Let's play Minesweeper! 💣")

    app = ConsoleApp(difficulty=difficulty, auto=args.auto)
