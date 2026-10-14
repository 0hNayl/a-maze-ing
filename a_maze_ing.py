from mazegen import MazeGenerator, NORTH, SOUTH, EAST, WEST

WALL_COLOR = "\033[48;2;200;200;200m"
PATH_COLOR = "\033[48;2;0;0;0m"
ENTRY_COLOR = "\033[48;2;0;183;235m"
EXIT_COLOR = "\033[48;2;255;0;255m"
RESET = "\033[0m"


def display_maze(maze: MazeGenerator) -> None:
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
                else:
                    color = PATH_COLOR
            elif screen_x % 2 == 0 and screen_y % 2 == 0:
                color = WALL_COLOR
            elif screen_y % 2 == 1:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if maze.grid[cell_y][cell_x] & WEST:
                    color = WALL_COLOR
                else:
                    color = PATH_COLOR
            else:
                cell_x = screen_x // 2
                cell_y = screen_y // 2
                if maze.grid[cell_y][cell_x] & NORTH:
                    color = WALL_COLOR
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
    display_maze(maze1)
