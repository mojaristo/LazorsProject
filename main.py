"""
Author: Jayden
main.py
Description: LazorGame class that ties reader, solver and writer together.
Usage: python main.py level.bff
"""
import sys
import time

from reader import BoardReader
from writer import SolutionWriter
from solver import LazorSolver


class LazorGame:
    """Loads a .bff level, solves it and writes <level>_solution.txt."""

    def __init__(self, path):
        self.path = path
        self.data = BoardReader(path).parse_file()
        self.solver = LazorSolver(self.data)
        self.solve_time = None

    def run(self):
        """Solve and save. Returns the solved grid of strings, or None."""
        start = time.perf_counter()
        solved = self.solver.solve()
        self.solve_time = time.perf_counter() - start

        if solved is None:
            print("No solution found.")
            print(f"Search time: {self.solve_time:.4f} seconds")
            return None

        grid = self.solver.to_grid()
        out = self.path.rsplit(".", 1)[0] + "_solution.txt"
        SolutionWriter(out).save_solution(grid, self.data["available_blocks"])
        for row in grid:
            print(" ".join(row))
        print(f"Solved in {self.solve_time:.4f} seconds")
        return grid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/level.bff")
        sys.exit(1)
    LazorGame(sys.argv[1]).run()
