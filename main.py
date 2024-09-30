# main file

from random import randint
import os

WIDTH, HEIGHT = 8, 8
CLEAR, RED, GREEN, YELLOW, BLUE = 0, 1, 2, 3, 4

DISPLAY_MODE = "cmd" # or win

colors = {
    CLEAR: "\033[30;40m  \033[0m",
    RED: "\033[31;41m  \033[0m",
    GREEN: "\033[32;42m  \033[0m",
    YELLOW: "\033[33;43m  \033[0m",
    BLUE: "\033[36;46m  \033[0m"
}

def afficher_grille(grille) -> None:
    """Print the game grid
    
    :param grille: the game grid"""
    """Display the game grid
    
    Depending on the global variable DISPLAY_MODE, it will render in the console or in an fltk window
    
    :param grille: game grid"""
    if DISPLAY_MODE == "cmd":
        print("  1 2 3 4 5 6 7 8")
        for i_row in range(len(grille)):
            print(chr(ord('a') + i_row), end=" ")
            for i_elem in range(len(grille[0])):
                print(colors[grille[i_row][i_elem]], end="")
            print()
    elif DISPLAY_MODE == "win":
        raise ValueError("Not implemented yet")
    else:
        raise ValueError("Incorrect display mode")


def check_capture(grid, x, y) -> list[tuple[int]]:
    """Check if a move at (x, y) for color player will capture some opponent pieces
    
    :param grid: the game grid
    :param x: the x coordinate of the move
    :param y: the y coordinate of the move
    :param color: the color of the player
    :return: a list of coordinates of the captured pieces"""
    color = grid[y][x]
    captures = []
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for dx, dy in directions:
        x_, y_ = x + dx, y + dy
        capture = []
        while (0 <= x_ < WIDTH) and (0 <= y_ < HEIGHT):
            if grid[y_][x_] in (CLEAR, color):
                break
            capture.append((x_, y_))
            x_, y_ = x_ + dx, y_ + dy
        if grid[y_][x_] == color:
            captures.extend(capture)
    return captures


def init_grid() -> list[list[str]]:
    """Initialize the game grid
    
    :return: the initialized game grid"""
    grid = [[CLEAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    grid[3][3] = RED
    grid[3][4] = YELLOW
    grid[4][3] = BLUE
    grid[4][4] = GREEN
    return grid


def play(grid, x, y, color) -> bool:
    """Play a move at (x, y) for color player
    
    :param grid: the game grid
    :param x: the x coordinate of the move
    :param y: the y coordinate of the move
    :param color: the color of the player
    :return: True if the move is valid, False otherwise"""
    if grid[y][x] != CLEAR:
        return False
    grid[y][x] = color
    captures = check_capture(grid, x, y)
    if len(captures) != 0:
        for x_, y_ in captures:
            grid[y_][x_] = color
    return True


def calc_score(grid) -> tuple[int, int, int, int]:
    """Calculate the final score for each players
    
    :return: The scores, in the order RED, YELLOW, GREEN, BLUE"""
    score_rouge = sum([grid[i].count(RED   ) for i in range(HEIGHT)])
    score_jaune = sum([grid[i].count(YELLOW) for i in range(HEIGHT)])
    score_vert  = sum([grid[i].count(GREEN ) for i in range(HEIGHT)])
    score_bleu  = sum([grid[i].count(BLUE  ) for i in range(HEIGHT)])

    return score_rouge, score_jaune, score_vert, score_bleu


def abcto123(letter) -> int:
    """Convert a letter to a number

    :param letter: the letter to convert
    :return: the corresponding number"""
    return int(ord(letter) - ord("a"))


def clear() -> None:
    """Clear the console"""
    os.system("cls" if os.name == "nt" else "clear")


def mainloop() -> None:
    """Main game loop"""
    # setup number of player and initial game state
    nb_players = 0
    while nb_players not in ("2", "3", "4"):
        nb_players = input("Combien de joueurs vont jouer ? [2-4] : ")
    nb_players = int(nb_players)
    
    print("Mettez vous d'accord sur vos couleurs ! Choisissez entre ", end="")
    if nb_players == 2:     print("rouge et vert.")
    elif nb_players == 3:   print("rouge, jaune et vert.")
    else:                   print("rouge, jeune, vert et bleu.")

    grid = init_grid()
    
    clear()
    afficher_grille(grid)

    for turn in range(60):
        player = turn % nb_players + 1
        coords=["", ""]
        while coords[0] not in ("a","b","c","d","e","f","g","h") or coords[1] not in ("1","2","3","4","5","6","7","8") or len(coords) > 2:
            playerInput = input(f"Joueur {str(player)}, Emplacement de votre prochaine boule (ex: a1, A1) : ").lower()
            if playerInput == "":
                continue
            coords = list(playerInput)
        x, y = int(coords[1]) - 1, abcto123(coords[0])
        played = play(grid, x, y, player)
        if not played:
            turn -= 1
            continue
        afficher_grille(grid)

    score_rouge, score_jaune, score_vert, score_bleu = calc_score(grid)
    print("Score final :")
    print("Rouge :", score_rouge)
    print("Jaune :", score_jaune)
    print("Vert :", score_vert)
    print("Bleu :", score_bleu)


if __name__ == "__main__":
    mainloop()