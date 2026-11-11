"""
Author: Jayden
solver.py
Description: LazorSolver class
"""
from itertools import combinations

from blocks import ReflectBlock, OpaqueBlock, RefractBlock
from tracer import LaserTracer


class LazorSolver:
    """Solves one level.

    data is the dict returned by BoardReader.parse_file(): grid,
    available_blocks, lasers, targets.
    """

    BLOCK_CLASSES = {'A': ReflectBlock, 'B': OpaqueBlock, 'C': RefractBlock}

    def __init__(self, data):
        self.grid = data["grid"]
        self.available_blocks = data["available_blocks"]
        self.lasers = data["lasers"]
        self.targets = set(data["targets"])
        self.board, self.free = self._build_board()
        self.tracer = LaserTracer(self.board, self.lasers)

    def _build_board(self):
        """Turn the string grid into Block/None cells.

        Pre-placed A/B/C cells become fixed Blocks, 'o' cells are recorded as
        free, and 'x' cells are never free.
        """
        board, free = [], []
        for r, row in enumerate(self.grid):
            out = []
            for c, ch in enumerate(row):
                cls = self.BLOCK_CLASSES.get(ch)
                out.append(cls(fixed=True) if cls else None)
                if ch == 'o':
                    free.append((r, c))
            board.append(out)
        return board, free

    def to_grid(self):
        """Current board as strings for SolutionWriter ('o'/'x' kept)."""
        return [[blk.block_type if blk else self.grid[r][c]
                 for c, blk in enumerate(row)]
                for r, row in enumerate(self.board)]

    @staticmethod
    def assignments(items, free):
        """Yield every way to put each (type, count) group into distinct cells."""
        if not items:
            yield []
            return
        (btype, n), rest_items = items[0], items[1:]
        for combo in combinations(free, n):
            taken = set(combo)
            remaining = [p for p in free if p not in taken]
            for tail in LazorSolver.assignments(rest_items, remaining):
                yield [(btype, combo)] + tail

    def solve(self):
        """Try every placement. Returns the solved board, or None.

        On success the blocks stay on self.board, so to_grid() shows the
        solution. On failure the board is left as it started.
        """
        items = list(self.available_blocks.items())
        for plan in self.assignments(items, self.free):
            placed = []
            for btype, cells in plan:
                for (r, c) in cells:
                    self.board[r][c] = self.BLOCK_CLASSES[btype](fixed=False)
                    placed.append((r, c))
            if self.tracer.hits_all(self.targets):
                return self.board
            for (r, c) in placed:
                self.board[r][c] = None
        return None