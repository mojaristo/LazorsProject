"""
Author: Kitan
writer.py
Description: Saves the solved Lazor board configuration to a text output file.
"""


class SolutionWriter:
    def __init__(self, output_filepath: str):
        """Writes the solved Lazor board layout to a file."""
        self.output_filepath = output_filepath

    def save_solution(self, solved_grid: list[list[str]], available_blocks_used: dict):
        """Writes the final solved grid and block placements to a text file."""
        with open(self.output_filepath, 'w') as file:
            file.write("# Lazor Game Solution\n")
            file.write("# Solved Board Layout:\n")
            file.write("GRID START\n")
            for row in solved_grid:
                file.write(" ".join(row) + "\n")
            file.write("GRID STOP\n")
            file.write("# Blocks used/placed:\n")
            for block_type, count in available_blocks_used.items():
                file.write(f"{block_type} {count}\n")

        print(f"Solution saved to {self.output_filepath}")