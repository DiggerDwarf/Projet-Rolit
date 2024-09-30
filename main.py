# main file

from random import randint
import os

WIDTH, HEIGHT = 8, 8
CLEAR, RED, YELLOW, GREEN, BLUE = 0, 1, 2, 3, 4

DISPLAY_MODE = "win" # or cmd
if DISPLAY_MODE == "win":
    from modules import fltk
    colors = {
        CLEAR: "#FFFFFF",
        RED: "#FF0000",
        GREEN: "#00FF00",
        YELLOW: "#FFFF00",
        BLUE: "#0000FF"
    }
else:
    colors = {
        CLEAR: "\033[30;40m  \033[0m",
        RED: "\033[31;41m  \033[0m",
        GREEN: "\033[32;42m  \033[0m",
        YELLOW: "\033[33;43m  \033[0m",
        BLUE: "\033[36;46m  \033[0m"
    }

def afficher_grille(grille: list[list[int]], player: int | None = None) -> None:
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
        fltk.efface_tout()
        fltk.rectangle(0,0,830,830, couleur=colors[player], remplissage="#000000", epaisseur=30)
        for i_row in range(len(grille)):
            for i_elem in range(len(grille[0])):
                fltk.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, colors[grille[i_row][i_elem]], remplissage=colors[grille[i_row][i_elem]])
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
    grid = [[CLEAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
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
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx, dy) == (0, 0):
                continue
            x_, y_ = x + dx, y + dy
            if (0 <= x_ < WIDTH) and (0 <= y_ < HEIGHT):
                if grid[y_][x_] != CLEAR:
                    return True
    return False


def play(grid, x, y, color) -> bool:
    """Play a move at (x, y) for color player
    
    :param grid: the game grid
    :param x: the x coordinate of the move
    :param y: the y coordinate of the move
    :param color: the color of the player
    :return: True if the move is valid, False otherwise"""
    if grid[y][x] != CLEAR or not test_adjacent(grid, x, y):
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
    """Convert a lowercase letter to a number

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
    if nb_players == 2:     print("rouge et jaune.")
    elif nb_players == 3:   print("rouge, jaune et vert.")
    else:                   print("rouge, jaune, vert et bleu.")


    grid = init_grid()

    if DISPLAY_MODE == "win":
        fltk.cree_fenetre("Rolit !", 830, 830, 60, False)
        tour = 0
        while True:
            # simple formula to get player index based on the number of players and the index of the turn
            player = tour % nb_players + 1
            afficher_grille(grid, player)
            
            # loop over events
            ev = fltk.donne_ev()
            while ev != None:
                match ev[0]:
                    case "Quitte":
                        # Pretty straightforward
                        fltk.ferme_fenetre()
                        return
                    case "ClicGauche":
                        # clamping the values to be in [0;800] then dividing by 100 (size of a spot) to get an index
                        i_column = (min(max(ev[1].x, 15), 815) - 15) // 100
                        i_row = (min(max(ev[1].y, 15), 815) - 15) // 100
                        
                        # if nothing's there, set the ball and advance to the next turn
                        if play(grid, i_column, i_row, player):
                            tour += 1
                        
                ev = fltk.donne_ev()
            fltk.mise_a_jour()
            
        
    elif DISPLAY_MODE == "cmd":
        while True:
            start = input("Voulez-vous commencer ? [O/n] : ").lower()
            if start == "o":
                break
            
        clear()
        afficher_grille(grid)

        for turn in range(60):
            player = turn % nb_players + 1
            played = False
            while not played:
                coords=["", ""]
                playerInput = input(f"Joueur {str(player)}, Emplacement de votre prochaine boule (ex: a1, A1) : ").lower()
                x_axis, y_axis = ("1","2","3","4","5","6","7","8"), ("a","b","c","d","e","f","g","h")
                if len(playerInput) != 2 or playerInput[0] not in y_axis or playerInput[1] not in x_axis: #check if input is valid (ex: a1, A1)
                    continue
                coords = list(playerInput)
                x, y = int(coords[1]) - 1, abcto123(coords[0])
                played = play(grid, x, y, player)
                if not played:
                    print("Coup invalide")
            afficher_grille(grid)

    score_rouge, score_jaune, score_vert, score_bleu = calc_score(grid)
    print("Score final :")
    print("Rouge :", score_rouge)
    print("Jaune :", score_jaune)
    print("Vert :", score_vert)
    print("Bleu :", score_bleu)


if __name__ == "__main__":
    mainloop()