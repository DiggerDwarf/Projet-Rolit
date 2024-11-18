# file to present
# Remove from this file all that is not needed for the first checkpoint

import os, argparse

WIDTH, HEIGHT = 8, 8
CLEAR, RED, YELLOW, GREEN, BLUE = 0, 1, 2, 3, 4

colors = {
    CLEAR: "\033[30;40m • \033[0m",
    RED: "\033[30;41m R \033[0m",
    GREEN: "\033[30;42m V \033[0m",
    YELLOW: "\033[30;43m J \033[0m",
    BLUE: "\033[30;46m B \033[0m"
}

color_names = {
    RED:    "rouge",
    YELLOW: "jaune",
    GREEN:  "vert",
    BLUE:   "bleu"
}


def display_grid_cmdline(grille: list[list[int]]) -> None:
    """Display the game grid onto the terminal
    
    :param grille: game grid"""
    # print column indices
    print("   1  2  3  4  5  6  7  8")
    for i_row in range(len(grille)):
        # print row indices
        print(chr(ord('a') + i_row), end=" ")
        # print ball colors according to lookup table `colors`
        for i_elem in range(len(grille[0])):
            print(colors[grille[i_row][i_elem]], end="")
        # print new line
        print()


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


def test_adjacent(grid, x, y) -> bool:
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


def calc_score(grid: list[list[int]]) -> tuple[int, int, int, int]:
    """Calculate the final score for each players
    
    :return: The scores, in the order RED, YELLOW, GREEN, BLUE"""
    # here we just sum up the amount of a color in each row, for each color.
    score_rouge = sum([grid[i].count(RED   ) for i in range(HEIGHT)])
    score_jaune = sum([grid[i].count(YELLOW) for i in range(HEIGHT)])
    score_vert  = sum([grid[i].count(GREEN ) for i in range(HEIGHT)])
    score_bleu  = sum([grid[i].count(BLUE  ) for i in range(HEIGHT)])

    return score_rouge, score_jaune, score_vert, score_bleu


def abcto123(letter: str) -> int:
    """Convert a lowercase letter to a number

    :param letter: the letter to convert
    :return: the corresponding number"""
    # calculate offset to lowercase a in the ASCII table
    return int(ord(letter) - ord("a"))


def clear() -> None:
    """Clear the console"""
    # just checking the os version to send correct clear command
    os.system("cls" if os.name == "nt" else "clear")



def mainloop_cmdline(nb_players: int, nb_manches: int) -> None:
    """Main game loop

    :param nb_players: number of players
    :param ai: if the player wants to play against the AI"""
    # setup number of player and initial game state
    if nb_players == 0:
        while nb_players not in ("2", "3", "4"):
            nb_players = input("Combien de joueurs vont jouer ? [2-4] : ")
        nb_players = int(nb_players)

    # tell player color roles according to nb of players
    print("Mettez vous d'accord sur vos couleurs ! Choisissez entre ", end="")
    if nb_players == 2:     print("rouge et jaune.")
    elif nb_players == 3:   print("rouge, jaune et vert.")
    else:                   print("rouge, jaune, vert et bleu.")

    grid = init_grid()
    
    print("Pour information, vous pouvez quitter le jeu à tout moment en écrivant 'q'.")
    # wait for players to choose a color before starting the game
    while True:
        start = input("Voulez-vous débuter la partie ? [O/n] : ").lower()
        if start == "o":
            break
        
    clear()
    display_grid_cmdline(grid)

    x_axis, y_axis = ("1","2","3","4","5","6","7","8"), ("a","b","c","d","e","f","g","h")
    for turn in range(60):
        # calculate player # based on simple formula
        player = turn % nb_players + 1
        # wait for correct input
        played = False
        while not played:
            # ask player for ball placement location
            playerInput = input(f"Joueur {color_names[player]}, Emplacement de votre prochaine boule (ex: a1, A1) : ").lower()
            if playerInput == 'q':
                return
            if len(playerInput) != 2 or playerInput[0] not in y_axis or playerInput[1] not in x_axis: #check if input is valid (ex: a1, A1)
                continue
            # convert player input to coordinates
            coords = list(playerInput)
            x, y = int(coords[1]) - 1, abcto123(coords[0])
            # attempt to play
            played = play(grid, x, y, player)
            # if it was evaluated to be an incorrect move, invalidate and try again
            if not played:
                print("Coup invalide")
                
        clear()
        display_grid_cmdline(grid)

    # after the game ends, calculate scores and print them
    score_rouge, score_jaune, score_vert, score_bleu = calc_score(grid)
    print("Score final :")
    print("Rouge :", score_rouge)
    print("Jaune :", score_jaune)
    print("Vert :", score_vert)
    print("Bleu :", score_bleu)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jeu de Rolit")
    
    # choose number of players from cmdline argument
    parser.add_argument("-n", "--nb_players", help="Nombre de joueurs", default=0, type=int)
    parser.add_argument("-m", "--nb_manches", help="Nombre de manches", default=1, type=int)
    
    args = parser.parse_args()
    
    if args.nb_players < 2 and args.nb_players != 0:
        print("Cannot have this little players, redirecting to choose prompt.")
        args.nb_players = 0
    elif args.nb_players > 4:
        print("Cannot have more than 4 players, truncating to 4.")
        args.nb_players = 4
    
    mainloop_cmdline(args.nb_players, args.nb_manches)