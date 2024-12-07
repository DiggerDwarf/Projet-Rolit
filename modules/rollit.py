"""All the functions needed for the Rollit game are here."""

from random import randint
from copy import deepcopy

WIDTH, HEIGHT = 8, 8 # grid size
CLEAR, RED, YELLOW, GREEN, BLUE = 0, 1, 2, 3, 4 # macros for colors
COLOR_NAMES = {
    RED:    "rouge",
    YELLOW: "jaune",
    GREEN:  "vert",
    BLUE:   "bleu"
}

def init_grid() -> list[list[str]]:
    """Initialize the game grid

    :return: the initialized game grid"""
    # create empty grid of correct size
    grid = [[CLEAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    # place start balls
    grid[3][3] = RED
    grid[3][4] = YELLOW
    grid[4][3] = BLUE
    grid[4][4] = GREEN
    return grid


def check_capture(grid: list[list[int]], x: int, y: int) -> list[tuple[int]]:
    """Check if a move at (x, y) for color player will capture some opponent pieces

    :param grid: the game grid
    :param x: the x coordinate of the move
    :param y: the y coordinate of the move
    :param color: the color of the player
    :return: a list of coordinates of the captured pieces"""
    # grab the color of the ball that was just placed
    color = grid[y][x]
    captures = []
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    if x == 0: # remove directions that are out of bounds
        directions = [d for d in directions if d[0] != -1]
    if x == WIDTH - 1:
        directions = [d for d in directions if d[0] != 1]
    if y == 0:
        directions = [d for d in directions if d[1] != -1]
    if y == HEIGHT - 1:
        directions = [d for d in directions if d[1] != 1]
    for dx, dy in directions:
        x_, y_ = x + dx, y + dy
        capture = []
        while (0 <= x_ < WIDTH) and (0 <= y_ < HEIGHT):
            if grid[y_][x_] in (CLEAR, color):
                break
            capture.append((x_, y_))
            x_, y_ = x_ + dx, y_ + dy
        if (0 <= x_ < WIDTH) and (0 <= y_ < HEIGHT) and grid[y_][x_] == color:
            captures.extend(capture)
    return captures


def test_adjacent(grid: list[list[int]], x: int, y: int) -> bool:
    """Test if there is any adjacent piece to (x, y) in the grid

    :param grid: the game grid
    :param x: the x coordinate
    :param y: the y coordinate
    :return: True if there is an adjacent piece, False otherwise"""
    # iterate over all 8 cardinal directions
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            # skip invalid null direction
            if (dx, dy) == (0, 0):
                continue
            # get new coordinates
            x_, y_ = x + dx, y + dy
            # check it isn't out of bounds
            if (0 <= x_ < WIDTH) and (0 <= y_ < HEIGHT):
                # if a ball is found in that direction, the placement is correct
                if grid[y_][x_] != CLEAR:
                    return True
    # if no direction succeeded, it must be incorrect
    return False


def play(grid: list[list[int]], x: int, y: int, color: int) -> bool:
    """Play a move at (x, y) for color player

    :param grid: the game grid
    :param x: the x coordinate of the move
    :param y: the y coordinate of the move
    :param color: the color of the player
    :return: True if the move is valid, False otherwise"""
    # invalidate placing over another ball and not adjacently to another ball
    if grid[y][x] != CLEAR or not test_adjacent(grid, x, y):
        return False
    # place the ball
    grid[y][x] = color
    # check what balls should be captured
    captures = check_capture(grid, x, y)
    # capture
    if len(captures) != 0:
        for x_, y_ in captures:
            grid[y_][x_] = color
    return True


def ai_play(grid: list[list[int]], color: int) -> tuple[int, int]:
    """Play a move for the AI

    :param grid: the game grid
    :param color: the color of the AI
    :return: the move played"""
    possible_moves = {}
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j] == CLEAR and test_adjacent(grid, j, i):
                test_grid = deepcopy(grid) # copy the grid to test the move
                test_grid[i][j] = color # play the move
                possible_moves[(j, i)] = len(check_capture(test_grid, j, i)) # calculate the amount of captures
    # get the best move(s) based on the amount of captures
    max_captures = max(possible_moves.values())
    best_moves = [k for k, v in possible_moves.items() if v == max_captures]
    move = best_moves[randint(0, len(best_moves) - 1)]
    play(grid, move[0], move[1], color)
    return move


def calc_score(grid: list[list[int]]) -> tuple[int, int, int, int]:
    """Calculate the final score for each players

    :return: The scores, in the order RED, YELLOW, GREEN, BLUE"""
    # here we just sum up the amount of a color in each row, for each color.
    score_rouge = sum([grid[i].count(RED   ) for i in range(HEIGHT)])
    score_jaune = sum([grid[i].count(YELLOW) for i in range(HEIGHT)])
    score_vert  = sum([grid[i].count(GREEN ) for i in range(HEIGHT)])
    score_bleu  = sum([grid[i].count(BLUE  ) for i in range(HEIGHT)])

    return score_rouge, score_jaune, score_vert, score_bleu