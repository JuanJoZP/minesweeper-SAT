import random
import argparse


class Game:

    def __init__(self, size=5, mines=3):
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mine_locations = []
        self.visible_board = [['-' for _ in range(size)] for _ in range(size)]
        self.flags = set()
        self.generate_mines()
        self.calculate_numbers()

    def generate_mines(self):
        while len(self.mine_locations) < self.mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in self.mine_locations:
                self.mine_locations.append((x, y))
                self.board[x][y] = 'M'

    def calculate_numbers(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M':
                    count = self.count_adjacent_mines(x, y)
                    self.board[x][y] = str(count)

    def count_adjacent_mines(self, x, y):
        count = 0
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if self.board[i][j] == 'M':
                    count += 1
        return count

    def display_board(self, board):
        for row in board:
            print(' '.join(row))

    def display_visible_board(self):
        self.display_board(self.visible_board)

    def display_full_board(self):
        print("\nGame Over! Here's the full board:")
        self.display_board(self.board)

    def reveal(self, x, y):
        if (x, y) in self.flags:
            print("This cell is flagged! Unflag to reveal.")
            return False
        if self.board[x][y] == 'M':
            self.display_full_board()
            return True
        elif self.visible_board[x][y] != '-':
            return False
        else:
            self.visible_board[x][y] = self.board[x][y]
            if self.board[x][y] == '0':
                self.reveal_adjacent(x, y)
        return False

    def reveal_adjacent(self, x, y):
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if self.visible_board[i][j] == '-' and self.board[i][j] != 'M':
                    self.reveal(i, j)

    def flag(self, x, y):
        if self.visible_board[x][y] != '-':
            print("This cell is already revealed.")
            return
        if (x, y) in self.flags:
            self.flags.remove((x, y))
            self.visible_board[x][y] = '-'
        else:
            self.flags.add((x, y))
            self.visible_board[x][y] = 'X'

    def play(self):
        while True:
            print(
                "Enter 'r' to reveal or 'f' to flag/unflag followed by row and column (e.g., 'r 0 1')"
            )
            self.display_visible_board()
            action = input("").split()

            if len(action) != 3 or action[0] not in ['r', 'f']:
                print(
                    "Invalid input. Use 'r' to reveal or 'f' to flag/unflag followed by row and column."
                )
                continue

            try:
                x, y = int(action[1]), int(action[2])
                if x < 0 or y < 0 or x >= self.size or y >= self.size:
                    print("Invalid coordinates. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter row and column numbers.")
                continue

            if action[0] == 'r':
                if self.reveal(x, y):
                    break  # Game over, player hit a mine
            elif action[0] == 'f':
                self.flag(x, y)

            # Check if all non-mine cells are revealed
            if all(self.visible_board[i][j] != '-'
                   for i in range(self.size)
                   for j in range(self.size)
                   if self.board[i][j] != 'M'):
                self.display_visible_board()
                print("Congratulations! You've cleared the board!")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Minesweeper!")
    parser.add_argument('--size',
                        type=int,
                        default=5,
                        help='Size of the board (default: 5)')
    parser.add_argument('--mines',
                        type=int,
                        default=3,
                        help='Number of mines (default: 3)')

    args = parser.parse_args()

    game = Game(size=args.size, mines=args.mines)
    game.play()
