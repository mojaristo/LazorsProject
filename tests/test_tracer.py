"""
test_tracer.py
Description: Unit tests for the LaserTracer class.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from blocks import ReflectBlock, OpaqueBlock, RefractBlock  # noqa: E402
from tracer import LaserTracer  # noqa: E402

# enters a 3x3 board from the top, heading down-left
LASER = [(3, 0, -1, 1)]


def empty_board(rows=3, cols=3):
    """Return a rows x cols board with no blocks on it."""
    return [[None] * cols for _ in range(rows)]


class TestBlockAhead(unittest.TestCase):
    """Tests for finding which block the laser is about to hit."""

    def test_vertical_edge_moving_left(self):
        board = empty_board()
        board[0][0] = ReflectBlock()
        blk, axis = LaserTracer(board, LASER).block_ahead(2, 1, -1, 1)
        self.assertIs(blk, board[0][0])
        self.assertEqual(axis, 'x')

    def test_horizontal_edge_moving_down(self):
        board = empty_board()
        board[1][0] = ReflectBlock()
        blk, axis = LaserTracer(board, LASER).block_ahead(1, 2, -1, 1)
        self.assertIs(blk, board[1][0])
        self.assertEqual(axis, 'y')

    def test_off_board_returns_none(self):
        blk, _ = LaserTracer(empty_board(), LASER).block_ahead(0, 1, -1, 1)
        self.assertIsNone(blk)


class TestTrace(unittest.TestCase):
    """Tests for following the laser across the board."""

    def test_empty_board_beam_passes_straight(self):
        visited = LaserTracer(empty_board(), LASER).trace()
        self.assertEqual(visited, {(3, 0), (2, 1), (1, 2), (0, 3)})

    def test_reflect_block_bounces_beam(self):
        board = empty_board()
        board[0][0] = ReflectBlock()
        visited = LaserTracer(board, LASER).trace()
        self.assertEqual(visited,
                         {(3, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)})

    def test_opaque_block_stops_beam(self):
        board = empty_board()
        board[0][0] = OpaqueBlock()
        self.assertEqual(LaserTracer(board, LASER).trace(), {(3, 0), (2, 1)})

    def test_refract_block_splits_beam(self):
        board = empty_board()
        board[0][0] = RefractBlock()
        visited = LaserTracer(board, LASER).trace()
        # straight-through half plus reflected half
        self.assertEqual(visited, {(3, 0), (2, 1), (1, 2), (0, 3),
                                   (3, 2), (4, 3), (5, 4), (6, 5)})

    def test_laser_start_point_counts_as_visited(self):
        self.assertIn((3, 0), LaserTracer(empty_board(), LASER).trace())

    def test_laser_starting_off_board_visits_nothing(self):
        tracer = LaserTracer(empty_board(), [(20, 20, 1, 1)])
        self.assertEqual(tracer.trace(), set())

    def test_multiple_lasers_are_combined(self):
        lasers = [(3, 0, -1, 1), (3, 6, -1, -1)]
        visited = LaserTracer(empty_board(), lasers).trace()
        self.assertIn((0, 3), visited)
        self.assertIn((3, 6), visited)

    def test_trace_does_not_modify_board(self):
        board = empty_board()
        board[0][0] = ReflectBlock()
        LaserTracer(board, LASER).trace()
        self.assertIsInstance(board[0][0], ReflectBlock)
        self.assertEqual(sum(b is not None for row in board for b in row), 1)

    def test_tracer_sees_blocks_placed_after_creation(self):
        board = empty_board()
        tracer = LaserTracer(board, LASER)
        self.assertIn((0, 3), tracer.trace())
        board[0][0] = OpaqueBlock()
        self.assertNotIn((0, 3), tracer.trace())


class TestHitsAll(unittest.TestCase):
    """Tests for checking that every target point is hit."""

    def test_true_when_all_targets_touched(self):
        tracer = LaserTracer(empty_board(), LASER)
        self.assertTrue(tracer.hits_all([(2, 1), (0, 3)]))

    def test_false_when_a_target_is_missed(self):
        tracer = LaserTracer(empty_board(), LASER)
        self.assertFalse(tracer.hits_all([(2, 1), (5, 0)]))


if __name__ == "__main__":
    unittest.main()
