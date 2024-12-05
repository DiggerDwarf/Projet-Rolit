# main file

from random import randint
import os, argparse
from copy import deepcopy
from time import sleep

WIDTH, HEIGHT = 8, 8
CLEAR, RED, YELLOW, GREEN, BLUE = 0, 1, 2, 3, 4
colors = {}
mainWindow = None

GRID=830
SIDE=330
SETTINGS=80

color_names = {
    RED:    "rouge",
    YELLOW: "jaune",
    GREEN:  "vert",
    BLUE:   "bleu"
}


def init_display(graphical: bool) -> None:
    """Initialize the display mode
    
    :param graphical: if the display is graphical or not"""
    global colors, mainWindow, colors_alt0, colors_alt1
    if graphical:
        # import graphics module and define colors as HEX codes
        from modules import fltk as mainWindow
        colors = {
            CLEAR: "#AED2FF",
            RED: "#FF004D",
            GREEN: "#00DFA2",
            YELLOW: "#FAEF5D",
            BLUE: "#0079FF"
        }
        colors_alt0 = {
            CLEAR: "#AED2FF",
            RED: "#FF004D",
            GREEN: "#00DFA2",
            YELLOW: "#FAEF5D",
            BLUE: "#0079FF"
        }
        colors_alt1 = {
            CLEAR: "#F8F8F2",
            RED: "#FF5555",
            GREEN: "#BD93F9", #Purple
            YELLOW: "#F1FA8C",
            BLUE: "#FF79C6" #Pink
        }
    else:
        # define colors as letters and ANSI escape codes
        colors = {
            CLEAR: "\033[40m • \033[0m",
            RED: "\033[30;41m R \033[0m",
            GREEN: "\033[30;42m V \033[0m",
            YELLOW: "\033[30;43m J \033[0m",
            BLUE: "\033[30;46m B \033[0m"
        }


def display_grid_window(grille: list[list[int]], player: int | None = None) -> None:
    """Display the game grid onto the fltk window
    
    :param grille: game grid"""
    mainWindow.efface_tout()
    # draw black background with an outline set as the current player's color
    mainWindow.rectangle(0,0,830,830, couleur=colors[player], remplissage="#222831", epaisseur=30)
    for i_row in range(len(grille)):
        for i_elem in range(len(grille[0])):
            # for each element of the game grid, draw circle of according color
            if grille[i_row][i_elem] == CLEAR and not test_adjacent(grille, i_elem, i_row): # If slot is unused and unreachable, fill in gray
                mainWindow.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, "#393E46", remplissage="#393E46")
            else: # Else, look in color lookup table
                mainWindow.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, colors[grille[i_row][i_elem]], remplissage=colors[grille[i_row][i_elem]])
    #40 pixels après la grille, on a le rectangle des scores qui lui va jusqu'à x=1160 sur 1200 de base, ensuite 60 pixels de plus pour paramètres
    mainWindow.rectangle(GRID+30,20,GRID+SIDE-30,80, couleur="#393E46", epaisseur=3) 
    #Affichage du header "Scores"
    mainWindow.texte((2*GRID+SIDE)/2,50,chaine="Scores", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25, tag="scores")
    mainWindow.image(GRID+SIDE+SETTINGS/3,50, fichier="settings.png", largeur=55, hauteur=55, ancrage="center", tag="setting-icon")

def menu_window_select(texts: tuple[str, str, str, str]) -> int:
    """Display a window with 4 choices and return the selected one
    
    :param texts: the texts to display on the window
    :return: the selected choice (1-4)"""
    mainWindow.efface_tout()
    mainWindow.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=colors[RED])
    mainWindow.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=colors[YELLOW])
    mainWindow.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=colors[BLUE])
    mainWindow.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=colors[GREEN])
    
    mainWindow.texte(207, 207, texts[0],   ancrage="center", police="consolas", taille=48)
    mainWindow.texte(622, 207, texts[1], ancrage="center", police="consolas", taille=48)
    mainWindow.texte(207, 622, texts[2], ancrage="center", police="consolas", taille=48)
    mainWindow.texte(622, 622, texts[3], ancrage="center", police="consolas", taille=48)
    
    mainWindow.texte(1060,50,chaine="<Règles ?> ", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)
    
    ev = None
    while True:
        mainWindow.mise_a_jour()
        ev = mainWindow.donne_ev()
        if ev is None: continue
        if ev[0] == "ClicGauche":
            if ev[1].x <= 415 and ev[1].y <= 415:
                return 1
            elif ev[1].x >= 415 and ev[1].y <= 415:
                return 2
            elif ev[1].x <= 415 and ev[1].y >= 415:
                return 3
            elif ev[1].x >= 415 and ev[1].y >= 415:
                return 4
        elif ev[0] == "Quitte":
            return -1


def display_end_window(scores: list[int]) -> None:
    """Display the end window with the final scores
    
    :param scores: the final scores of each player"""
    mainWindow.efface_tout()
    mainWindow.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=colors[RED])
    mainWindow.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=colors[YELLOW])
    mainWindow.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=colors[BLUE])
    mainWindow.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=colors[GREEN])
    
    crown_x = 415 * (max(scores) == scores[1] or max(scores) == scores[3])
    crown_y = 415 * (max(scores) == scores[2] or max(scores) == scores[3])
    
    mainWindow.PIL_AVAILABLE = False
    mainWindow.image(crown_x, crown_y, "crown_perfect_size.png", largeur=415, hauteur=415, ancrage="nw")
    
    mainWindow.texte(207, 207, str(scores[0]), ancrage="center", police="consolas", taille=128)
    mainWindow.texte(622, 207, str(scores[1]), ancrage="center", police="consolas", taille=128)
    mainWindow.texte(207, 622, str(scores[2]), ancrage="center", police="consolas", taille=128)
    mainWindow.texte(622, 622, str(scores[3]), ancrage="center", police="consolas", taille=128)
    
    mainWindow.texte(1060,50,chaine="<Félicitations ?> ", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)
    mainWindow.texte(1060,80,chaine="<Scores de manches ?>", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)

    ev = None
    while True:
        mainWindow.mise_a_jour()
        ev = mainWindow.donne_ev()
        if ev is None: continue
        if ev[0] == "ClicGauche":
            return
        elif ev[0] == "Quitte":
            return -1

    
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


def clear() -> None:
    """Clear the console"""
    # just checking the os version to send correct clear command
    os.system("cls" if os.name == "nt" else "clear")


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


def mainloop_window(nb_players: int, nb_manches: int, ai: bool) -> None:
    """Main game loop

    :param nb_players: number of players
    :param ai: if the player wants to play against the AI"""
    global colors, colors_alt0, colors_alt1
    # create the game window
    mainWindow.cree_fenetre(GRID+SIDE+SETTINGS, GRID, 60, False)

    ok = False # if all choices are done
    while not ok:
        if nb_players == 0: # if the player didn't choose the number of players, select the number of players
            choice = menu_window_select(("1 JOUEUR", "2 JOUEURS", "3 JOUEURS", "4 JOUEURS"))
            if choice == -1:
                return
            nb_players = choice
        if nb_players == 1: # if the player selected one player, enable AI mode
            choice = menu_window_select(("RETOUR", "1 IA", "2 IAs", "3 IAs"))
            if choice == -1:
                return
            if choice == 1:
                nb_players = 0
                continue
            nb_players = choice
            ai = True
        if nb_manches == 0: # if the player didn't choose the number of rounds, select the number of rounds
            choice = menu_window_select(("1 MANCHE", "2 MANCHES", "3 MANCHES", "4 MANCHES"))
            if choice == -1:
                return
            nb_manches = choice
        ok = True
    
    for _ in range(nb_manches):
        player_bias = randint(0, 4)
        grid = init_grid()
        tour = 0
        while tour < 60:
            # simple formula to get player index based on the number of players and the index of the turn
            player = (tour + player_bias) % nb_players + 1
            display_grid_window(grid, player)
            
            # loop over events
            ev = mainWindow.donne_ev()
            while ev != None:
                match ev[0]:
                    case "Quitte":
                        # Pretty straightforward
                        mainWindow.ferme_fenetre()
                        return
                    case "ClicGauche":
                        # clamping the values to be in [0;800] then dividing by 100 (size of a spot) to get an index
                        i_column = (min(max(ev[1].x, 15), 815) - 15) // 100
                        i_row = (min(max(ev[1].y, 15), 815) - 15) // 100
                        
                        i_column = min(max(i_column, 0), 7)
                        i_row = min(max(i_row, 0), 7)
                        
                        
                        # if nothing's there, set the ball and advance to the next turn
                        if play(grid, i_column, i_row, player):
                            tour += 1
                            # AI mode is single-player
                            # so after the player has played, if ai mode is enabled, make them play
                            if ai:
                                # display player move, update the window and wait before making the IAs play
                                display_grid_window(grid, player)
                                mainWindow.mise_a_jour()
                                sleep(1)
                                # there are `nb_players - 1` IAs knowing there's 1 real player
                                for _ in range(nb_players-1):
                                    # get current IA player id
                                    player = (tour + player_bias) % nb_players + 1
                                    # make them play
                                    ai_play(grid, player)
                                    tour += 1
                                    # between each IA turn, display and wait
                                    display_grid_window(grid, player)
                                    mainWindow.mise_a_jour()
                                    mainWindow.__canevas.ev_queue.clear()
                                    sleep(1)
                    case "Touche":
                        if colors == colors_alt0:
                            colors = colors_alt1
                        elif colors == colors_alt1:
                            colors = colors_alt0
                        
                # grab next event
                ev = mainWindow.donne_ev()
            # update the window after event handling
            mainWindow.mise_a_jour()

        # after the game has ended, calculate the score and print it
        score_rouge, score_jaune, score_vert, score_bleu = calc_score(grid)
        
        if display_end_window([score_rouge, score_jaune, score_bleu, score_vert]) == -1:
            mainWindow.ferme_fenetre()
            return

def mainloop_cmdline(nb_players: int, nb_manches: int, ai: bool) -> None:
    """Main game loop

    :param nb_players: number of players
    :param nb_manches: number of rounds
    :param ai: if the player wants to play against the AI"""
    # setup number of player and initial game state

    clear()
    if nb_players == 0:
        while nb_players not in ("2", "3", "4"):
            nb_players = input("Combien de joueurs vont jouer ? [2-4] : ")
        nb_players = int(nb_players)

    if nb_manches == 0:
        nb_manches = input("Combien de manches voulez-vous jouer ? (par défaut 1): ")
        if nb_manches.isnumeric():
            nb_manches = int(nb_manches)
        else:
            nb_manches = 1


    if ai: # if the player wants to play against the AI
        print("Vous allez jouer contre l'IA")
        print("Vous êtes rouge")
    else:
        # tell player color roles according to nb of players
        print("Mettez vous d'accord sur vos couleurs ! Choisissez entre ", end="")
        if nb_players == 2:     print("rouge et jaune.")
        elif nb_players == 3:   print("rouge, jaune et vert.")
        else:                   print("rouge, jaune, vert et bleu.")

    score_tot = { #total of scores in case of draw
        RED: 0,
        YELLOW: 0,
        GREEN: 0,
        BLUE: 0
    }

    rounds_won = {
        RED: 0,
        YELLOW: 0,
        GREEN: 0,
        BLUE: 0
    }
    
    for i in range(nb_manches):
        print(f"--- MANCHE N°{i+1} ---")
        print("Pour information, vous pouvez quitter le jeu à tout moment en écrivant 'q'.")
        # wait for players to choose a color before starting the game
        while True:
            start = input("Voulez-vous débuter la partie ? [O/n] : ").lower()
            if start == "o" or start == "":
                break
            elif start == "q":
                return

        grid = init_grid() #init grid for each rounds   

        clear()
        display_grid_cmdline(grid)

        x_axis, y_axis = ("1","2","3","4","5","6","7","8"), ("a","b","c","d","e","f","g","h")
        for turn in range(60):
            # calculate player # based on simple formula
            player = turn % nb_players + 1
            # wait for correct input
            played = False
            while not played:
                if (ai and player == RED) or not ai: # ai or player turn and if not against ai always ask for input
                    # ask player for ball placement location
                    playerInput = input(f"Joueur {color_names[player]}, Emplacement de votre prochaine boule (ex: a1, A1) : ").lower()
                    if playerInput == "q":
                        return
                    if len(playerInput) == 2 and playerInput[0] in y_axis and playerInput[1] in x_axis: #check if input is valid (ex: a1, A1)
                        # convert player input to coordinates
                        coords = list(playerInput)
                        x, y = int(coords[1]) - 1, int(ord(coords[0]) - ord("a"))
                        # attempt to play
                        played = play(grid, x, y, player)
                    # if it was evaluated to be an incorrect move, invalidate and try again
                    if not played:
                        print("Coup invalide")
                else:
                    move = ai_play(grid, player)
                    clear()
                    display_grid_cmdline(grid)
                    print(f"L'IA a joué en {chr(ord('a') + move[1])}{move[0] + 1}")
                    os.system("pause")
                    played = True
            clear()
            display_grid_cmdline(grid)

        # after the game ends, calculate scores and print them
        score_round = calc_score(grid)
        print("Score de la manche :")
        print("Rouge :", score_round[0])
        print("Jaune :", score_round[1])
        print("Vert :", score_round[2])
        print("Bleu :", score_round[3])

        score_tot[RED] += score_round[0]
        score_tot[YELLOW] += score_round[1]
        score_tot[GREEN] += score_round[2]
        score_tot[BLUE] += score_round[3]

        #get the max score and the player who won the round
        max_score = max(score_round)
        winner = [p for i, p in enumerate(score_tot.keys()) if score_round[i] == max_score]

        if len(winner) == 1:
            print(f"Le gagnant de la manche est le joueur {color_names[winner[0]]} avec {max_score} points !")
        else:
            print(f"Egalité entre les joueurs", end=" ")
            for p in winner:
                print(color_names[p], end=" ")
            print(f"avec un score de {max_score} pour la manche")
        rounds_won[winner[0]] += 1

    #get the max score and the player who won the game
    max_score = max(score_tot.values())
    winner = [k for k, v in score_tot.items() if v == max_score]
    if len(winner) == 1:
        print(f"Le gagnant de la partie est le joueur {color_names[winner[0]]} avec {max_score} points !")
    else:
        print(f"Egalité entre les joueurs", end=" ")
        for p in winner:
            print(color_names[p], end=" ")
        print(f"avec un score de {max_score} pour la partie")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jeu de Rolit")
    # choose display mode from cmdline argument
    parser.add_argument("--graphical", help="Mode graphique", default=True, type=bool, action=argparse.BooleanOptionalAction)
    # choose number of players from cmdline argument
    parser.add_argument("-n", "--nb_players", help="Nombre de joueurs", default=0, type=int)
    # choose number of rounds to play
    parser.add_argument("-m", "--nb_manches", help="Nombre de manches", default=0, type=int)
    # choose if the player wants to play against the AI
    parser.add_argument("--ai", help="Jouer contre l'IA", default=False, type=bool, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    init_display(args.graphical)
    
    if args.nb_players < 2 and args.nb_players != 0:
        print("Cannot have this little players, redirecting to choose prompt")
        args.nb_players = 0
    elif args.nb_players > 4:
        print("Cannot have more than 4 players, truncating to 4.")
        args.nb_players = 4
    
    # enter correct game loop based on dislpay mode
    if args.graphical:
        mainloop_window (args.nb_players, args.nb_manches, args.ai)
    else:
        mainloop_cmdline(args.nb_players, args.nb_manches, args.ai)
