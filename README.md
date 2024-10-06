# Minesweeper SAT Solver

Welcome to the **Minesweeper SAT Solver**, a project that tackles the classic Minesweeper game using logical techniques! By translating the game into a SAT (Satisfiability) problem, this solver can automatically find solutions based on the given board's configuration.

## How does it work?

This project solves Minesweeper by transforming the board and its rules at a given round into a SAT problem. It generates the complete truth table (very slow for large boards) and retrieves all the satisfiable interpretations to then calculate probabilities for mines locations. Then with these probabilities it proceeds to uncover or flag cells acordingly.

## Installation

To get started, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/JuanJoZP/minesweeper-SAT.git
   cd minesweeper-SAT
   ```
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Running the Program

To run the solver, simply execute `python main.py --auto`

If you want to handle uncertain decisions yourself and have delays between steps (for better visualization), remove the --auto argument.

Once the game starts, follow the instructions in the console. The app will guide you through interacting with the game in various configurations.
