"""
Author: Kitan
reader.py
Description: Parses Lazor .bff game files into structured data for the
solver and tracer.
"""


class BoardReader:
    """Reads and parses .bff level files for the Lazor game."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.grid = []
        self.available_blocks = {}
        self.lasers = []
        self.targets = []

    def parse_file(self):
        """Reads the .bff file and extracts the board configuration."""
        with open(self.filepath, "r") as f:
            lines = f.readlines()
        mode = None
        for line in lines:
            # strip whitespace
            line = line.strip()
            # ignore comments
            if line.startswith("#"):
                continue
            # ignore empty lines
            if not line:
                continue
            # check for the start of the grid
            if line == "GRID START":
                mode = "GRID"
                continue
            # check for the end of the grid
            elif line == "GRID STOP":
                mode = None
                continue

            # split grid rows by spaces and add them to the grid
            if mode == "GRID":
                row = line.split()
                self.grid.append(row)
                continue

            parts = line.split()
            # parse available blocks
            if parts[0] in ['A', 'B', 'C'] and len(parts) == 2:
                block_type = parts[0]
                count = int(parts[1])
                self.available_blocks[block_type] = count

            # parse lasers: L x y vx vy
            elif parts[0] == "L" and len(parts) == 5:
                x, y, vx, vy = map(int, parts[1:])
                self.lasers.append((x, y, vx, vy))

            # parse targets: P x y
            elif parts[0] == "P" and len(parts) == 3:
                x, y = map(int, parts[1:])
                self.targets.append((x, y))

        return {
            "grid": self.grid,
            "available_blocks": self.available_blocks,
            "lasers": self.lasers,
            "targets": self.targets,
        }
