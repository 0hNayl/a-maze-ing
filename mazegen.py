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

"42" pattern:
    A set of fully closed cells drawing "42", centred so that the
    empty column between the "4" and the "2" lies on the centre cell.
    These cells are marked as visited before generation, so the
    algorithm never opens them.
"""
import random
from collections import deque

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

LETTERS = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W"
}
OPPOSITES = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

PATTERN_42: tuple[str, ...] = (
    "#.#.###",
    "#.#...#",
    "###.###",
    "..#.#..",
    "..#.###",
)
PATTERN_MARGIN = 1


class MazeGenerator:
    """Generate a maze on a grid of cells."""

    def __init__(self, width: int, height: int, maze_entry: tuple[int, int],
                 maze_exit: tuple[int, int], seed: int | None = None) -> None:
        """Create a grid with every wall closed.

        Args:
            width: maze width in cells.
            height: maze height in cells.
            maze_entry: entry cell (x, y).
            maze_exit: exit cell (x, y).
            seed: seed of the created grid

        Raises:
            ValueError: if entry or exit is outside the maze, inside
                the "42" pattern, or if they are the same cell.
        """
        self.width: int = width
        self.height: int = height
        entry_x, entry_y = maze_entry
        exit_x, exit_y = maze_exit
        if not (0 <= entry_x < self.width and 0 <= entry_y < self.height):
            raise ValueError(f"entry {maze_entry} is outside the maze")
        if not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
            raise ValueError(f"exit {maze_exit} is outside the maze")
        if maze_entry == maze_exit:
            raise ValueError("Entry and exit values must be different")
        self.entry = maze_entry
        self.exit = maze_exit
        self.pattern: set[tuple[int, int]] = self.compute_pattern()
        if maze_entry in self.pattern:
            raise ValueError(f"entry {maze_entry} is inside the 42 pattern")
        if maze_exit in self.pattern:
            raise ValueError(f"exit {maze_exit} is inside the 42 pattern")
        self._rng: random.Random = random.Random(seed)
        self.reset()

    def compute_pattern(self) -> set[tuple[int, int]]:
        """Compute the cells of the "42" pattern, centred on the maze.

        Returns:
            The set of (x, y) cells to keep fully closed, or an empty
            set if the maze is too small to hold the pattern and its
            margin.
        """
        pattern_w = len(PATTERN_42[0])
        pattern_h = len(PATTERN_42)
        offset_x = self.width // 2 - pattern_w // 2
        offset_y = self.height // 2 - pattern_h // 2
        if (offset_x < PATTERN_MARGIN
                or offset_y < PATTERN_MARGIN
                or offset_x + pattern_w + PATTERN_MARGIN > self.width
                or offset_y + pattern_h + PATTERN_MARGIN > self.height):
            return set()
        cells: set[tuple[int, int]] = set()
        for pattern_y, row in enumerate(PATTERN_42):
            for pattern_x, char in enumerate(row):
                if char == "#":
                    cells.add((offset_x + pattern_x, offset_y + pattern_y))
        return cells

    def has_pattern(self) -> bool:
        """Tell whether the maze is big enough to contain the pattern."""
        return bool(self.pattern)

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
        """Backtracking to mine all the paths and generate a perfect maze"""
        self.reset()
        self.visited.update(self.pattern)
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

    def open_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        """Check open neighbors cells"""
        availables: list[tuple[int, int, int]] = []
        for direction, (diff_x, diff_y) in DELTAS.items():
            neib_x = x + diff_x
            neib_y = y + diff_y
            if (0 <= neib_x < self.width and
                    0 <= neib_y < self.height and
                    not (self.grid[y][x] & direction)):
                availables.append((neib_x, neib_y, direction))
        return availables

    def solve(self) -> list[tuple[int, int]]:
        queue = deque([self.entry])
        parents: dict[tuple[int, int], tuple[int, int] | None] = {
            self.entry: None
        }
        while queue:
            current = queue.popleft()
            if current == self.exit:
                break
            x, y = current
            for neib_x, neib_y, direction in self.open_neighbors(x, y):
                if (neib_x, neib_y) not in parents:
                    parents[(neib_x, neib_y)] = current
                    queue.append((neib_x, neib_y))
        path = []
        if self.exit not in parents:
            return []
        cell: tuple[int, int] | None = self.exit
        while cell is not None:
            path.append(cell)
            cell = parents[cell]
        path.reverse()
        return path

    def to_text(self, path: list[tuple[int, int]]) -> str:
        lines = []
        for row in self.grid:
            lines.append("".join(format(cell, "X") for cell in row))
        lines.append("")
        lines.append(f"{self.entry[0]},{self.entry[1]}")
        lines.append(f"{self.exit[0]},{self.exit[1]}")
        path_text = []
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            diff_x = x2 - x1
            diff_y = y2 - y1
            path_text.append(LETTERS[(diff_x, diff_y)])
        lines.append("".join(path_text))
        return "\n".join(lines) + "\n"
