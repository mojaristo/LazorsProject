# LazorsProject

A solver for the Lazors puzzle game. Given a level file (`.bff`), it finds where to place the available blocks so that the laser beams pass through every target point, then writes the solved board to a text file.

**Authors:** Kitan Lawal and Jayden Kgobe

## Quick start
### Requirements 
- Python 3.9 or newer 
- All the project files kept together in one folder: `main.py`, `blocks.py`, `reader.py`, `writer.py`, `tracer.py`, `solver.py`, `your_file_name.bff`


### Running from PyCharm
1. Open the project folder in PyCharm.
2. Go to **Run > Edit Configurations**, select `main` .
3. In **Parameters**, enter your file `your_file_name.bff`.
4. Make sure **Working directory** is the project folder, so the relative path is found.
5. Click **OK**, then run.

### Running from a terminal
Run `main.py` and give it the path to a level file (`.bff`):
```
python main.py your_file_name.bff
```
## The game in brief

A level is a grid of cells. Lasers shine across the board, and the goal is to light up every target point. You get a fixed number of blocks to place on empty cells:

| Letter | Block | Effect on a laser |
|---|---|---|
| `A` | Reflect | Bounces the beam |
| `B` | Opaque | Absorbs the beam |
| `C` | Refract | Bounces the beam and lets a copy pass straight through |

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
## The level file format (example)

```
GRID START
o o o o B o
o o o o B o
o o o o o o
o o o o o o
C o o o o o
o o o x x x
GRID STOP

A 4            # 4 reflect blocks available
C 1            # 1 refract block available
L 7 6 1 1      # laser: x, y, vx, vy
P 3 12         # target point the beam must pass through
```

Lines starting with `#` are comments. `BoardReader.parse_file()` returns a dict with four entries: `grid` (a list of rows of letters), `available_blocks` (`{'A': 4, 'C': 1}`), `lasers` (a list of `(x, y, vx, vy)`), and `targets` (a list of `(x, y)`).

## How the code solves a level

The pipeline in `main.py` is: **read, build the board, search, write**.

### 1. Reading

`BoardReader` turns the `.bff` file into the dict described above as a plain string

### 2. Building the board (`LazorSolver._build_board`)

The solver converts the string grid into a board of `Block` objects and `None` for empty cells:

- Pre-placed `A`/`B`/`C` cells become `Block` objects with `fixed=True`.
- `o` cells become `None` and are recorded in a list of **free cells**, the only places the solver may put blocks.
- `x` cells become `None` but are *not* free, so they stay empty forever.

### 3. The coordinate system

Lasers and targets live on a lattice that is **twice as fine as the grid**.

For a grid with `R` rows and `C` columns, points have `x` in `0..2C` and `y` in `0..2R`. Cell `(row r, col c)` covers `x` from `2c` to `2c+2` and `y` from `2r` to `2r+2`.

Every point a laser can be located in has one even and one odd coordinate: it sits at the middle of a cell edge. A point with an even `x` is on a vertical edge between two cells; a point with an even `y` is on a horizontal edge. Because beams always move diagonally (`vx` and `vy` are each `+1` or `-1`), a step changes both coordinates by one, so the one-even-one-odd property is kept as the beam travels.

### 4. Tracing a laser (`LaserTracer`)

`LaserTracer.trace()` returns the set of all lattice points the beams touch. For each beam, it repeats:

1. Record the current point as visited.
2. Look at the cell the beam is about to enter (`block_ahead`).
   - On a vertical edge (even `x`) that is the cell to the left or right, depending on the sign of `vx`.
   - On a horizontal edge (even `y`) that is the cell above or below, depending on the sign of `vy`.
   - Cells outside the grid count as empty.
3. React to the block there:
   - **No block:** step to `(x + vx, y + vy)`.
   - **Opaque (`B`):** the beam does not continue (stops).
   - **Reflect (`A`):** flip `vx` if the beam hits a vertical edge, or `vy` if it hits a horizontal one, then check again from the same point.
   - **Refract (`C`):** queue a copy of the beam that carries straight on through the block, then reflect the original as above.
4. Stop when the beam leaves the board.


- After a reflection the beam re-checks the cell on its new side, so a beam caught between two blocks reflects off both properly.
- A set of already-seen states `(x, y, vx, vy)` stops the loop if beams ever cycle, so tracing always terminates.

`hits_all(targets)` is simply "are all targets inside the visited set?"

### 5. Searching (`LazorSolver.solve`)

The solver tries every possible arrangement of the available blocks:

1. `assignments()` generates every way to choose distinct free cells for each block type. It uses `itertools.combinations` once per type, so two identical `A` blocks swapped between the same two cells count as a single arrangement.
2. For each arrangement the solver places the blocks on the board, asks the tracer whether every target is hit, and removes the blocks again if not.
3. The first arrangement that works is returned, and its blocks stay on the board so `to_grid()` can convert it back to letters for the writer.

If nothing works, the board is left as it started and `solve()` returns `None`.

### 6. Writing

`LazorGame.run()` converts the board back to strings (keeping `o` and `x` from the input) and hands it to `SolutionWriter`, which saves it to `<your_file_name>_solution.txt`.

## Tests

`tests/test_tracer.py` covers beam behaviour: empty boards, each block type, multiple lasers, start points, and that blocks placed after the tracer is created are noticed. `tests/test_solver.py` covers board building, arrangement generation, solving (including an unsolvable level), and the full `LazorGame` run. 


