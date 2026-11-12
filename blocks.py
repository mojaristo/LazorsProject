"""
Author: Kitan
blocks.py
Description: Defines the base block class and specific block types for the game
"""

class Block:
    """A standard block in the game."""
    def __init__(self, block_type, fixed=False):
        self.block_type = block_type  # 'A' (reflect), 'B' (opaque), or 'C' (refract)
        self.fixed = fixed            # True if it's locked in place on the starting board


class ReflectBlock(Block):
    """Reflects the laser."""
    def __init__(self, fixed=False):
        super().__init__('A', fixed)


class OpaqueBlock(Block):
    """Blocks the laser completely."""
    def __init__(self, fixed=False):
        super().__init__('B', fixed)


class RefractBlock(Block):
    """Splits the laser (reflects and passes through)."""
    def __init__(self, fixed=False):
        super().__init__('C', fixed)