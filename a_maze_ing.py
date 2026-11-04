import sys

from mazegen import MazeGenerator, NORTH, WEST

WALL_COLOR = "\033[48;2;200;200;200m"
PATH_COLOR = "\033[48;2;0;0;0m"
ENTRY_COLOR = "\033[48;2;48;92;222m"
EXIT_COLOR = "\033[48;2;224;175;255m"
SOLUTION_COLOR = "\033[48;2;100;149;237m"
PATTERN_COLOR = "\033[48;2;255;105;180m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

WALL_COLORS = [
    WALL_COLOR,
    "\033[48;2;70;130;220m",
    "\033[48;2;60;170;90m",
    "\033[48;2;200;80;80m",
]
MENU = ("=== A-Maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show/Hide path from entry to exit\n"
        "3. Rotate maze colors\n"
        "4. Quit")


def display_maze(maze: MazeGenerator,
                 path: list[tuple[int, int]] = [],
                 wall_color: str = WALL_COLOR) -> None:
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
                color = wall_color
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
                    color = wall_color
            elif screen_y % 2 == 1:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if ((cell_x, cell_y) in maze.pattern
                        and (cell_x - 1, cell_y) in maze.pattern):
                    color = PATTERN_COLOR
                elif maze.grid[cell_y][cell_x] & WEST:
                    color = wall_color
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
                    color = wall_color
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


def run(maze: MazeGenerator) -> None:
    """Display the maze and handle the user's choices."""
    maze.generate()
    path = maze.solve()
    show_path = False
    color = 0
    message = ""
    while True:
        print(CLEAR, end="")
        display_maze(maze, path if show_path else [], WALL_COLORS[color])
        print(MENU)
        print(message)
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        message = ""
        if choice == "1":
            maze.generate()
            path = maze.solve()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color = (color + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            message = "Invalid choice, type 1 to 4."


if __name__ == "__main__":
    try:
        maze1 = MazeGenerator(20, 10, (2, 4), (7, 9))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    if not maze1.has_pattern():
        print("Error: maze too small to draw the 42 pattern",
              file=sys.stderr)
    run(maze1)
