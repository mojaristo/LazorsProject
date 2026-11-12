"""
Author: Kitan
reader.py
Description: Parses Lazor.bff game files into structured data for the solver and tracer.
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
        """reads the .bff file and extracts the board configuration"""
        with open(self.filepath, "r") as f:
            lines = f.readlines()
        mode = None
        for line in lines:
            line = line.strip() #strips whitespace
            if line.startswith("#"): #ignores comments
                continue
            if not line: #ignore empty line
                continue
            if line == "GRID START": #checks for grid start
                mode = "GRID"
                continue
            elif line == "GRID STOP": #checks for end of grid
                mode = None
                continue

            if mode == "GRID": #splits rows by spaces and adds to grid
                row = line.split()
                self.grid.append(row)
                continue

            parts = line.split()
            if parts[0] in ['A', 'B', 'C'] and len(parts) == 2: # Parses available blocks
                block_type = parts[0]
                count = int(parts[1])
                self.available_blocks[block_type] = count
            elif parts[0] == 'L' and len(parts) == 5: # Parses lasers
                x, y, vx, vy = map(int, parts[1:])
                self.lasers.append((x, y, vx, vy))
            elif parts[0] == 'P' and len(parts) == 3: # Parses targets
                x, y = map(int, parts[1:])
                self.targets.append((x, y))

        return {
            "grid": self.grid,
            "available_blocks": self.available_blocks,
            "lasers": self.lasers,
            "targets": self.targets
        }
