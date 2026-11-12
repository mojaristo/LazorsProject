"""
test_writer.py
Author: Kitan Lawal
Description: Clean, fresh unit test for the SolutionWriter class.
"""
import os

from writer import SolutionWriter


def test_solution_writer():
    """Test that SolutionWriter creates and writes a solution file."""
    filename = "test_solution_output.txt"
    solved_grid = [
        ['A', 'o', 'B'],
        ['o', 'C', 'o'],
        ['B', 'o', 'A']
    ]
    blocks_used = {'A': 2, 'C': 1}

    # create the writer instance and save the solution
    writer = SolutionWriter(filename)
    writer.save_solution(solved_grid, blocks_used)

    # check that the file was written (it is saved inside solutions/)
    file_exists = os.path.exists(writer.output_filepath)
    assert file_exists, "The solution file was not created!"

    # clean up the temporary file
    os.remove(writer.output_filepath)

    print("✅ SolutionWriter test passed successfully!")


if __name__ == "__main__":
    test_solution_writer()
