"""
Author: Jayden
tracer.py
Description: LaserTracer class that follows laser beams across a board of
Block objects.

Coordinates: a grid with R rows and C columns has laser/target points on a
doubled lattice, x in 0..2C and y in 0..2R. Cell (row r, col c) occupies
x in [2c, 2c+2] and y in [2r, 2r+2]. Every point a laser can be on has exactly
one even and one odd coordinate (the middle of a cell edge).
"""


class LaserTracer:
    """Traces lasers over a board.

    The tracer keeps a reference to the board (it does not copy it), so a
    solver can place and remove blocks and call trace() again each time.
    """

    def __init__(self, board, lasers):
        """board: list of rows of Block or None. lasers: list of (x, y, vx, vy)."""
        self.board = board
        self.lasers = lasers

    def block_ahead(self, x, y, vx, vy):
        """Return (block, axis) for the cell the beam is about to enter.

        axis is 'x' if the beam meets a vertical edge (flip vx) and 'y' if a
        horizontal edge (flip vy). block is None for an empty cell or a cell
        off the board.
        """
        rows, cols = len(self.board), len(self.board[0])
        if x % 2 == 0:                      # on a vertical edge
            r, c, axis = y // 2, (x // 2 if vx > 0 else x // 2 - 1), 'x'
        else:                               # on a horizontal edge
            r, c, axis = (y // 2 if vy > 0 else y // 2 - 1), x // 2, 'y'
        if 0 <= r < rows and 0 <= c < cols:
            return self.board[r][c], axis
        return None, axis

    def trace(self):
        """Follow every laser and return the set of lattice points touched.

        A reflect block ('A') flips the beam, an opaque block ('B') stops it,
        and a refract block ('C') flips it while a copy continues straight
        through.
        """
        rows, cols = len(self.board), len(self.board[0])
        visited, seen = set(), set()
        stack = list(self.lasers)
        while stack:
            x, y, vx, vy = stack.pop()
            while (0 <= x <= 2 * cols and 0 <= y <= 2 * rows
                   and (x, y, vx, vy) not in seen):
                seen.add((x, y, vx, vy))
                visited.add((x, y))
                blk, axis = self.block_ahead(x, y, vx, vy)
                if blk is None:
                    x, y = x + vx, y + vy
                    continue
                kind = blk.block_type
                if kind == 'B':
                    break
                if kind == 'C':
                    stack.append((x + vx, y + vy, vx, vy))
                # reflect (A, and the reflected half of C), re-check this point
                if axis == 'x':
                    vx = -vx
                else:
                    vy = -vy
        return visited

    def hits_all(self, targets):
        """True if every target point is touched by a beam."""
        return set(targets) <= self.trace()