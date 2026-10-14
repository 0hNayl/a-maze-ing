"""Reusable maze generation module.

Grid layout:
    The grid is indexed as grid[y][x], rows first.
    y increases southwards (downwards on screen).

Wall encoding:
    Each cell is an integer whose bits define its walls.
    A bit set to 1 means the wall is closed.
    Bit 0 = north, bit 1 = east, bit 2 = south, bit 3 = west.
    The resulting value (0 to 15) is the hexadecimal digit
    written to the output file.
"""
import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST

DELTAS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0)
}

OPPOSITES = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}


class MazeGenerator:
    """Generate a maze on a grid of cells."""

    def __init__(self, width: int, height: int, maze_entry: tuple[int, int],
                 maze_exit: tuple[int, int], seed: int | None = None) -> None:
        """Create a grid with every wall closed.

        Args:
            width: maze width in cells.
            height: maze height in cells.
            seed: seed of the created grid
        """
        self.width: int = width
        self.height: int = height
        self.entry = maze_entry
        self.exit = maze_exit
        entry_x, entry_y = maze_entry
        exit_x, exit_y = maze_exit
        if not (0 <= entry_x < self.width and 0 <= entry_y < self.height):
            raise ValueError(f"entry {maze_entry} is outside the maze")
        if not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
            raise ValueError(f"exit {maze_exit} is outside the maze")
        if maze_entry == maze_exit:
            raise ValueError("Entry and exit values must be different")
        self._rng: random.Random = random.Random(seed)
        self.reset()

    def reset(self) -> None:
        """Clear the grid and the visited set."""
        self.visited: set[tuple[int, int]] = set()
        self.grid: list[list[int]] = [[ALL_WALLS for _ in range(self.width)]
                                      for _ in range(self.height)]

    def mine(self, x: int, y: int, direction: int) -> None:
        """Break the wall between 2 cells in a given direction"""
        diff_x, diff_y = DELTAS[direction]
        neighbor_x = x + diff_x
        neighbor_y = y + diff_y
        self.grid[y][x] = self.grid[y][x] & (ALL_WALLS - direction)
        opposite = OPPOSITES[direction]
        self.grid[neighbor_y][neighbor_x] = (self.grid[neighbor_y][neighbor_x]
                                             & (ALL_WALLS - opposite))

    def available_moves(self, x: int, y: int) -> list[tuple[int, int, int]]:
        """Checks the already visited cells and returns all available moves"""
        moves: list[tuple[int, int, int]] = []
        for direction, (diff_x, diff_y) in DELTAS.items():
            neib_x = x + diff_x
            neib_y = y + diff_y
            if (0 <= neib_x < self.width and
                    0 <= neib_y < self.height and
                    (neib_x, neib_y) not in self.visited):
                moves.append((neib_x, neib_y, direction))
        return moves

    def generate(self) -> None:
        self.reset()
        start: tuple[int, int] = self.entry
        self.visited.add(start)
        stack: list[tuple[int, int]] = [start]
        while stack:
            x, y = stack[-1]
            moves = self.available_moves(x, y)
            if not moves:
                stack.pop()
            else:
                way = self._rng.choice(moves)
                next_x, next_y, mine_direction = way
                self.mine(x, y, mine_direction)
                self.visited.add((next_x, next_y))
                stack.append((next_x, next_y))
