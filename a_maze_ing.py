import sys

from mazegen import MazeGenerator, NORTH, WEST

WALL_COLOR = "\033[48;2;200;200;200m"
PATH_COLOR = "\033[48;2;0;0;0m"
ENTRY_COLOR = "\033[48;2;48;92;222m"
EXIT_COLOR = "\033[48;2;224;175;255m"
SOLUTION_COLOR = "\033[48;2;100;149;237m"
PATTERN_COLOR = "\033[48;2;130;130;130m"
RESET = "\033[0m"
REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")


def display_maze(maze: MazeGenerator, path: list[tuple[int, int]] = []) -> None:
    for screen_y in range(2 * maze.height + 1):
        chars = []
        for screen_x in range(2 * maze.width + 1):
            if screen_x % 2 == 1:
                cell_width = 4
            else:
                cell_width = 2
            if (screen_x == 0
                    or screen_y == 0
                    or screen_x == 2 * maze.width
                    or screen_y == 2 * maze.height):
                color = WALL_COLOR
            elif screen_x % 2 == 1 and screen_y % 2 == 1:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if (cell_x, cell_y) in maze.pattern:
                    color = PATTERN_COLOR
                elif (cell_x, cell_y) == maze.entry:
                    color = ENTRY_COLOR
                elif (cell_x, cell_y) == maze.exit:
                    color = EXIT_COLOR
                elif (cell_x, cell_y) in path:
                    color = SOLUTION_COLOR
                else:
                    color = PATH_COLOR
            elif screen_x % 2 == 0 and screen_y % 2 == 0:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                around = {(cell_x - 1, cell_y - 1), (cell_x, cell_y - 1),
                          (cell_x - 1, cell_y), (cell_x, cell_y)}
                if around <= maze.pattern:
                    color = PATTERN_COLOR
                else:
                    color = WALL_COLOR
            elif screen_y % 2 == 1:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if ((cell_x, cell_y) in maze.pattern
                        and (cell_x - 1, cell_y) in maze.pattern):
                    color = PATTERN_COLOR
                elif maze.grid[cell_y][cell_x] & WEST:
                    color = WALL_COLOR
                elif (cell_x, cell_y) in path and (cell_x - 1, cell_y) in path:
                    color = SOLUTION_COLOR
                else:
                    color = PATH_COLOR
            else:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if ((cell_x, cell_y) in maze.pattern
                        and (cell_x, cell_y - 1) in maze.pattern):
                    color = PATTERN_COLOR
                elif maze.grid[cell_y][cell_x] & NORTH:
                    color = WALL_COLOR
                elif (cell_x, cell_y) in path and (cell_x, cell_y - 1) in path:
                    color = SOLUTION_COLOR
                else:
                    color = PATH_COLOR
            chars.append(color + " " * cell_width)
        chars.append(RESET)
        if screen_y % 2 == 1:
            repeat = 2
        else:
            repeat = 1
        for _ in range(repeat):
            print("".join(chars))


def read_config(filename: str) -> dict[str, str]:
    config: dict[str, str] = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            parts = line.split("=", 1)
            if len(parts) != 2:
                raise ValueError(f"invalid line in config: {line}")
            key = parts[0].strip()
            value = parts[1].strip()
            config[key] = value
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"missing key in config: {key}")
    return config


def to_int(key: str, value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"invalid integer for {key}: {value}")


def to_cell(key: str, value: str) -> tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"invalid cell for {key}: {value}")
    return (to_int(key, parts[0].strip()), to_int(key, parts[1].strip()))


def to_bool(key: str, value: str) -> bool:
    value = value.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    else:
        raise ValueError(f"invalid bool for {key}: {value}")

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    try:
        config = read_config(sys.argv[1])
        width = to_int("WIDTH", config["WIDTH"])
        height = to_int("HEIGHT", config["HEIGHT"])
        entry = to_cell("ENTRY", config["ENTRY"])
        exit_cell = to_cell("EXIT", config["EXIT"])
        perfect = to_bool("PERFECT", config["PERFECT"])
        output_file = config["OUTPUT_FILE"]
        maze1 = MazeGenerator(width, height, entry, exit_cell)
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    if not maze1.has_pattern():
        print("Error: maze too small to draw the 42 pattern",
              file=sys.stderr)
    maze1.generate()
    path = maze1.solve()
    try:
        with open(output_file, "w") as f:
            f.write(maze1.to_text(path))
    except OSError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    display_maze(maze1, path)
