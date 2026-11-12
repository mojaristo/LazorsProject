# LazorsProject

A solver for the Lazors puzzle game. Given a level file (`.bff`), it finds where to place the available blocks so that the laser beams pass through every target point, then writes the solved board to a text file.

## Quick start

```
python main.py/*.bff
```
## The game in brief

A level is a grid of cells. Lasers shine across the board, and the goal is to light up every target point. You get a fixed number of blocks to place on empty cells:

| Letter | Block | Effect on a laser |
|---|---|---|
| `A` | Reflect | Bounces the beam |
| `B` | Opaque | Absorbs the beam |
| `C` | Refract | Bounces the beam *and* lets a copy pass straight through |

Grid cells are `o` (a block may go here), `x` (no block allowed), or `A`/`B`/`C` (a block that is already placed and fixed).


## Project layout

```
blocks.py    Block, ReflectBlock, OpaqueBlock, RefractBlock   (Kitan)
reader.py    BoardReader: parses a .bff file                  (Kitan)
writer.py    SolutionWriter: saves the solved board           (Kitan)
tracer.py    LaserTracer: follows beams across a board        (Jayden)
solver.py    LazorSolver: searches for a winning block layout (Jayden)
main.py      LazorGame: command-line entry point              (Jayden)
tests/       unit tests and sample levels
```
##
