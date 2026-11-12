"""
test_reader.py
Author: Kitan Lawal
Description: Tests for block classes and BoardReader.
"""

from blocks import ReflectBlock, OpaqueBlock, RefractBlock
from reader import BoardReader
import os

def test_blocks():
    """Test that our block classes create correctly."""
    r_block = ReflectBlock(fixed=True)
    assert r_block.block_type == 'A'
    assert r_block.fixed == True

    o_block = OpaqueBlock(fixed=False)
    assert o_block.block_type == 'B'
    assert o_block.fixed == False

    c_block = RefractBlock(fixed=False)
    assert c_block.block_type == 'C'
    assert c_block.fixed == False

    print("✅ Block tests passed successfully!")


def test_board_reader():
    """Test that our BoardReader can successfully create and read a fake .bff file."""
    filename = "test_level.bff"
    test_content = """
GRID START
o x o
x o x
o x o
GRID STOP

A 2
C 1

L 0 0 1 -1
P 2 2
"""

    with open(filename, "w") as f:
        f.write(test_content)
    reader = BoardReader(filename)
    data = reader.parse_file()

    # Checking that everything was read correctly
    assert data is not None, "The reader returned nothing!"
    assert len(data["grid"]) == 3, "The grid rows count is incorrect!"
    assert data["available_blocks"] == {'A': 2, 'C': 1}, "The available blocks were parsed incorrectly!"

    if os.path.exists(filename): #cleans up temporary data file
        os.remove(filename)

    print("✅ BoardReader test passed successfully!")


if __name__ == "__main__":
    test_blocks()
    test_board_reader()