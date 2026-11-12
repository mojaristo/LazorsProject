"""
Author: Jayden
main.py
Description: LazorGame class that ties reader, solver and writer together.
Usage: python main.py level.bff
"""
import sys

from reader import BoardReader
from writer import SolutionWriter
from solver import LazorSolver


class LazorGame:
    """Loads a .bff level, solves it and writes <level>_solution.txt."""

    def __init__(self, path):
        self.path = path
        self.data = BoardReader(path).parse_file()
        self.solver = LazorSolver(self.data)

    def run(self):
        """Solve and save. Returns the solved grid of strings, or None."""
        if self.solver.solve() is None:
            print("No solution found.")
            return None
        grid = self.solver.to_grid()
        out = self.path.rsplit(".", 1)[0] + "_solution.txt"
        SolutionWriter(out).save_solution(grid, self.data["available_blocks"])
        for row in grid:
            print(" ".join(row))
        return grid


if __name__ == "__main__":
    LazorGame(sys.argv[1]).run()