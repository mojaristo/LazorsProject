"""
test_writer.py
Author: Kitan Lawal
Description: Clean, fresh unit test for the SolutionWriter class.
"""

from writer import SolutionWriter
import os

def test_solution_writer():
    """Test that SolutionWriter can successfully create and write a solution file."""
    filename = "test_solution_output.txt"
    solved_grid = [
        ['A', 'o', 'B'],
        ['o', 'C', 'o'],
        ['B', 'o', 'A']
    ]
    blocks_used = {'A': 2, 'C': 1}

    writer = SolutionWriter(filename) #Creates the writer instance and save the solution
    writer.save_solution(solved_grid, blocks_used)
    file_exists = os.path.exists(filename)  #Checks that the file was successfully written to your folder
    assert file_exists == True, "The solution file was not created!"

    if file_exists: #cleans up temporary data file
        os.remove(filename)

    print("✅ SolutionWriter test passed successfully!")

if __name__ == "__main__":
    test_solution_writer()