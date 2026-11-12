import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))

from blocks import Block
from reader import BoardReader
from solver import LazorSolver
from main import LazorGame

LEVELS = os.path.join(HERE, "levels")


def load(name):
    return BoardReader(os.path.join(LEVELS, name)).parse_file()


def level(name):
    return LazorSolver(load(name))


class TestBuildBoard(unittest.TestCase):
    def setUp(self):
        grid = [["o", "A"], ["x", "o"]]
        self.solver = LazorSolver({"grid": grid, "available_blocks": {},
                                   "lasers": [], "targets": []})

    def test_fixed_blocks_are_marked_fixed(self):
        blk = self.solver.board[0][1]
        self.assertIsInstance(blk, Block)
        self.assertEqual(blk.block_type, "A")
        self.assertTrue(blk.fixed)

    def test_x_cells_are_not_free(self):
        self.assertNotIn((1, 0), self.solver.free)
        self.assertIsNone(self.solver.board[1][0])

    def test_free_cells_are_only_o(self):
        self.assertEqual(self.solver.free, [(0, 0), (1, 1)])

    def test_to_grid_round_trips(self):
        self.assertEqual(self.solver.to_grid(), self.solver.grid)


class TestAssignments(unittest.TestCase):
    def test_counts_match_combinations(self):
        plans = list(LazorSolver.assignments([("A", 1), ("C", 1)],
                                             [(0, 0), (0, 1), (0, 2)]))
        self.assertEqual(len(plans), 3 * 2)

    def test_no_cell_used_twice(self):
        free = [(0, i) for i in range(4)]
        for plan in LazorSolver.assignments([("A", 2), ("C", 1)], free):
            cells = [c for _, combo in plan for c in combo]
            self.assertEqual(len(cells), len(set(cells)))

    def test_no_blocks_gives_one_empty_plan(self):
        self.assertEqual(list(LazorSolver.assignments([], [(0, 0)])), [[]])


class TestSolve(unittest.TestCase):
    def test_simple_level_is_solved(self):
        solver = level("simple_3x3.bff")
        self.assertIsNotNone(solver.solve())
        self.assertTrue(solver.tracer.hits_all(solver.targets))

    def test_example_6x6_hits_every_target(self):
        solver = level("example_6x6.bff")
        self.assertIsNotNone(solver.solve())
        self.assertTrue(solver.tracer.hits_all(solver.targets))

    def test_unsolvable_level_returns_none(self):
        self.assertIsNone(level("unsolvable.bff").solve())

    def test_failed_solve_leaves_board_unchanged(self):
        solver = level("unsolvable.bff")
        before = solver.to_grid()
        solver.solve()
        self.assertEqual(solver.to_grid(), before)

    def test_solution_uses_exact_block_counts(self):
        solver = level("example_6x6.bff")
        board = solver.solve()
        placed = {}
        for row in board:
            for blk in row:
                if blk is not None and not blk.fixed:
                    placed[blk.block_type] = placed.get(blk.block_type, 0) + 1
        self.assertEqual(placed, solver.available_blocks)

    def test_solution_keeps_fixed_blocks_and_x_cells(self):
        solver = level("example_6x6.bff")
        solver.solve()
        grid = solver.to_grid()
        for r, row in enumerate(solver.grid):
            for c, ch in enumerate(row):
                if ch != "o":
                    self.assertEqual(grid[r][c], ch)


class TestLazorGame(unittest.TestCase):
    def test_run_writes_solution_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "level.bff")
            with open(os.path.join(LEVELS, "simple_3x3.bff")) as src:
                text = src.read()
            with open(path, "w") as dst:
                dst.write(text)
            grid = LazorGame(path).run()
            out = os.path.join(tmp, "level_solution.txt")
            self.assertTrue(os.path.exists(out))
            self.assertEqual(grid[0][0], "A")
            with open(out) as f:
                self.assertIn("GRID START", f.read())

    def test_run_returns_none_when_unsolvable(self):
        path = os.path.join(LEVELS, "unsolvable.bff")
        self.assertIsNone(LazorGame(path).run())
        self.assertFalse(os.path.exists(path.replace(".bff", "_solution.txt")))


if __name__ == "__main__":
    unittest.main()