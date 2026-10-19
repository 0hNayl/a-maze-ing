from mazegen import MazeGenerator, NORTH, SOUTH, EAST, WEST

WALL_COLOR = "\033[48;2;200;200;200m"
PATH_COLOR = "\033[48;2;0;0;0m"
ENTRY_COLOR = "\033[48;2;48;92;222m"
EXIT_COLOR = "\033[48;2;224;175;255m"
SOLUTION_COLOR = "\033[48;2;100;149;237m"
RESET = "\033[0m"
PATTERN_42 = "X..X.XXXX", "X..X....X", "XXXX.XXXX", "...X.X...", "...X.XXXX",


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
                if (cell_x, cell_y) == maze.entry:
                    color = ENTRY_COLOR
                elif (cell_x, cell_y) == maze.exit:
                    color = EXIT_COLOR
                elif (cell_x, cell_y) in path:
                    color = SOLUTION_COLOR
                else:
                    color = PATH_COLOR
            elif screen_x % 2 == 0 and screen_y % 2 == 0:
                color = WALL_COLOR
            elif screen_y % 2 == 1:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if maze.grid[cell_y][cell_x] & WEST:
                    color = WALL_COLOR
                elif (cell_x, cell_y) in path and (cell_x - 1, cell_y) in path:
                    color = SOLUTION_COLOR
                else:
                    color = PATH_COLOR
            else:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if maze.grid[cell_y][cell_x] & NORTH:
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


if __name__ == "__main__":
    maze1 = MazeGenerator(20, 10, (4, 2), (9, 9))
    maze1.generate()
    path = maze1.solve()
    print(len(path), path[0], path[-1])
    display_maze(maze1, path)
    for line in PATTERN_42:
        print(line)
