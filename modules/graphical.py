"""Graphical game"""

from modules.rollit import *
from time import sleep
import modules.fltk_dev as mainWindow
import modules.saver as saver

# graphical display variables
GRID = 830 # ui elements width
SIDE = 330
SETTINGS = 80
QUARTER = (GRID+SIDE+SETTINGS)/4
PADDING = 20
BASE_BAR_X = 860 # base coordinates for the score bars
BASE_BAR_Y = 200
BAR_HEIGHT = 50 # height of the score bars
BAR_VERTICAL_SPACING = 10 # spacing between score bars
MAX_BAR_WIDTH = SIDE-40

ALL_COLORS = [
    {
        CLEAR: "#AED2FF",
        RED: "#FF004D",
        GREEN: "#00DFA2",
        YELLOW: "#FAEF5D",
        BLUE: "#0079FF"
    },
    {
        CLEAR: "#F8F8F2",
        RED: "#FF5555",
        GREEN: "#BD93F9", #Purple
        YELLOW: "#F1FA8C",
        BLUE: "#FF79C6" #Pink
    }
]
COLORS_LIST = ["CLEAR","RED","GREEN","YELLOW","BLUE"]
COLOR_INDEX = 0
SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

def display_grid_window(grid: list[list[int]], player: int | None = None, current_scores: list[int] | None = None) -> None:
    """Display the game grid onto the fltk window and side informations
    
    :param grid: game grid
    :param player: the current player
    :param current_scores: the current scores of each player"""
    mainWindow.efface_tout()
    # draw black background with an outline set as the current player's color
    mainWindow.rectangle(0,0,830,830, couleur=SELECTED_COLORS[player], remplissage="#222831", epaisseur=30)
    for i_row in range(len(grid)):
        for i_elem in range(len(grid[0])):
            # for each element of the game grid, draw circle of according color
            if grid[i_row][i_elem] == CLEAR and not test_adjacent(grid, i_elem, i_row): # If slot is unused and unreachable, fill in gray
                mainWindow.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, "#393E46", remplissage="#393E46")
            else: # Else, look in color lookup table
                mainWindow.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, SELECTED_COLORS[grid[i_row][i_elem]], remplissage=SELECTED_COLORS[grid[i_row][i_elem]])
    # Re draw background for side view
    mainWindow.rectangle(GRID, 0, GRID+SIDE, GRID, couleur="#F0F0F0", remplissage="#F0F0F0")

    # Draw the score header outline
    mainWindow.rectangle(BASE_BAR_X-10, 20, BASE_BAR_X+MAX_BAR_WIDTH+10, 810, epaisseur=5)
    # Affichage du header "Scores"
    mainWindow.texte(GRID+SIDE/2+10,50,chaine="Scores", ancrage="center", police="Cascadia Code", taille=25)
    mainWindow.image(GRID+SIDE+(SETTINGS-55)/2, 20, fichier="assets/settings.png", largeur=55, hauteur=55, ancrage="nw", tag="setting-icon")

    if current_scores:
        max_score = max(current_scores)
        for i in range(max(len(current_scores), 4)):
            bar_y = BASE_BAR_Y + (BAR_HEIGHT + BAR_VERTICAL_SPACING) * i # calculate the y coordinate of the bar
            bar_width = (current_scores[i] / max_score)*MAX_BAR_WIDTH # calculate the width of the bar
            mainWindow.rectangle(BASE_BAR_X, bar_y, BASE_BAR_X + bar_width, bar_y + BAR_HEIGHT, epaisseur=5, remplissage=SELECTED_COLORS[i+1])
            mainWindow.texte(BASE_BAR_X+10, bar_y, str(current_scores[i]), ancrage="nw", police="Cascadia Code", taille=25)
            if current_scores[i] == max_score:
                mainWindow.image(BASE_BAR_X+MAX_BAR_WIDTH-60, bar_y, "assets/crown_perfect_size.png", largeur=50, hauteur=50, ancrage="nw") # add a crown for the leading player


def display_end_window(scores: list[int]) -> None:
    """Display the end window with the final scores

    :param scores: the final scores of each player"""
    mainWindow.efface_tout()
    mainWindow.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[RED])
    mainWindow.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[YELLOW])
    mainWindow.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[BLUE])
    mainWindow.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[GREEN])

    crown_x = 415 * (max(scores) == scores[1] or max(scores) == scores[3])
    crown_y = 415 * (max(scores) == scores[2] or max(scores) == scores[3])

    mainWindow.PIL_AVAILABLE = False
    mainWindow.image(crown_x, crown_y, "assets/crown_perfect_size.png", largeur=415, hauteur=415, ancrage="nw")

    mainWindow.texte(207, 207, str(scores[0]), ancrage="center", police="Cascadia Code", taille=128)
    mainWindow.texte(622, 207, str(scores[1]), ancrage="center", police="Cascadia Code", taille=128)
    mainWindow.texte(207, 622, str(scores[2]), ancrage="center", police="Cascadia Code", taille=128)
    mainWindow.texte(622, 622, str(scores[3]), ancrage="center", police="Cascadia Code", taille=128)

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


def menu_window_select(texts: tuple[str, str, str, str]) -> int:
    """Display a window with 4 choices and return the selected one
    
    :param texts: the texts to display on the window
    :return: the selected choice (1-4)"""
    mainWindow.efface_tout()
    mainWindow.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[RED])
    mainWindow.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[YELLOW])
    mainWindow.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[BLUE])
    mainWindow.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[GREEN])

    mainWindow.texte(207, 207, texts[0], ancrage="center", police="Cascadia Code", taille=48)
    mainWindow.texte(622, 207, texts[1], ancrage="center", police="Cascadia Code", taille=48)
    mainWindow.texte(207, 622, texts[2], ancrage="center", police="Cascadia Code", taille=48)
    mainWindow.texte(622, 622, texts[3], ancrage="center", police="Cascadia Code", taille=48)

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


def submenu_title(x1: int, y1: int, x2: int, y2: int, text: str = "Submenu") -> None:
    """Display a submenu title
    
    :param x1: the x coordinate of the top left corner
    :param y1: the y coordinate of the top left corner
    :param x2: the x coordinate of the bottom right corner
    :param y2: the y coordinate of the bottom right corner
    :param text: the text to display"""
    mainWindow.rectangle(x1, y1, x2, y2, epaisseur=5)
    mainWindow.texte((x1+x2)/2, (y1+y2)/2, text, ancrage="center", police="Cascadia Code", taille=25)


def theme_btn(i: int) -> int:
    """Display a button for a theme

    :param i: the index of the theme
    :return: the id of the button"""
    start_x = QUARTER + PADDING
    end_x = 2*QUARTER - PADDING
    out = mainWindow.rectangle(start_x, 150 + i*70, end_x, 200 + i*70, epaisseur=5, remplissage="#123456")
    for j in range(5):
        mainWindow.rectangle(
            ax = (start_x + 2.5) + j*(end_x - start_x - 5)/5,
            ay = 150 + i*70 + 2.5,
            bx = (start_x + 2.5) + (j + 1)*(end_x - start_x - 5)/5,
            by = 200 + i*70 - 2.5,
            couleur = ALL_COLORS[i][j],
            remplissage = ALL_COLORS[i][j],
            epaisseur = 0
        )
    return out


def themes() -> list[int]:
    """Theme selection buttons

    :return: the list of ids of the buttons"""
    out = []
    for i in range(len(ALL_COLORS)):
        out.append(theme_btn(i))
    return out


def settings_menu() -> tuple[str, int]:
    """Display the settings menu
    
    :return: the selected option"""
    mainWindow.efface_tout()
    submenu_title(PADDING-10, 40, QUARTER-PADDING+10, 100, "Règles")
    submenu_title(QUARTER+PADDING-10, 40, 2*QUARTER-PADDING+10, 100, "Thèmes")
    submenu_title(2*QUARTER+PADDING-10, 40, 3*QUARTER-PADDING+10, 100, "Accessibilité")
    submenu_title(3*QUARTER+PADDING-10, 40, 4*QUARTER-PADDING+10, 100, "Sauvegarde")
    theme_boxes = themes()
    while True:
        evName, evData = mainWindow.attend_ev()
        match evName:
            case "Quitte":
                return ("quit", -1)
            case "ClicGauche":
                for i in range(len(theme_boxes)):
                    if mainWindow.est_objet_survole(theme_boxes[i]):
                        mainWindow.rectangle(QUARTER+PADDING, 150 + i*70, 2*QUARTER-PADDING, 200 + i*70, epaisseur=8, couleur=ALL_COLORS[i][GREEN])
                        return ("theme", i)


def mainloop(nb_players: int, nb_rounds: int, ai: bool) -> None:
    """Main game loop

    :param nb_players: number of players
    :param nb_rounds: number of rounds
    :param ai: if the player wants to play against the AI"""
    global ALL_COLORS, COLOR_INDEX, SELECTED_COLORS

    # create the game window
    mainWindow.cree_fenetre(GRID+SIDE+SETTINGS, GRID, 60, False)

    ok = False # if all choices are done
    while not ok:
        if nb_players == 0: # if the player didn't choose the number of players, select the number of players
            choice = menu_window_select(("1 Joueur", "2 Joueurs", "3 Joueurs", "4 Joueurs"))
            if choice == -1:
                return
            nb_players = choice
        if nb_players != 0: # when player number is selected, select ai number
            choice = menu_window_select(("Aucune IA", "1 IA", "2 IA", "3 IA"))
            if choice == -1:
                return
            if (choice-1) + nb_players > 4:
                continue
            nb_ai = choice - 1
            ai = True
        if nb_rounds == 0: # if the player didn't choose the number of rounds, select the number of rounds
            choice = menu_window_select(("1 Manche", "2 Manches", "3 Manches", "4 Manches"))
            if choice == -1:
                return
            nb_rounds = choice
        ok = True

    for _ in range(nb_rounds):
        player_bias = randint(0, 4)
        grid = init_grid()
        tour = 0
        while tour < 60:
            # simple formula to get player index based on the number of players and the index of the turn
            player = (tour + player_bias) % (nb_players + nb_ai) + 1
            display_grid_window(grid, player, calc_score(grid))
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
                        i_column = (ev[1].x - 15) // 100
                        i_row = (ev[1].y - 15) // 100

                        # if nothing's there, set the ball and advance to the next turn
                        if 0 <= i_column <= 7 and 0 <= i_row <= 7 and play(grid, i_column, i_row, player):
                            tour += 1
                            if ai and (tour % (nb_players + nb_ai)) == nb_players:
                                # display player move, update the window and wait before making the IAs play
                                display_grid_window(grid, player, calc_score(grid))
                                mainWindow.mise_a_jour()
                                sleep(1)
                                for _ in range(nb_ai):
                                    # get current IA player id
                                    player = (tour + player_bias) % (nb_players + nb_ai) + 1
                                    # make them play
                                    ai_play(grid, player)
                                    tour += 1
                                    # between each IA turn, display and wait
                                    display_grid_window(grid, player, calc_score(grid))
                                    mainWindow.mise_a_jour()
                                    mainWindow.__canevas.ev_queue.clear()
                                    sleep(1)
                        elif GRID+SIDE<ev[1].x<GRID+SIDE+SETTINGS and 10<ev[1].y<80:
                            param_out = settings_menu()
                            match param_out[0]:
                                case "quit":
                                    mainWindow.ferme_fenetre()
                                    return
                                case "theme":
                                    COLOR_INDEX = param_out[1]
                                    SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

                    case "Touche":
                        print(saver.unpack_grid(saver.pack_grid(grid)) == grid)

                # grab next event
                ev = mainWindow.donne_ev()
            # update the window after event handling
            mainWindow.mise_a_jour()

        # after the game has ended, calculate the score and print it
        score_rouge, score_jaune, score_vert, score_bleu = calc_score(grid)

        if display_end_window([score_rouge, score_jaune, score_bleu, score_vert]) == -1:
            mainWindow.ferme_fenetre()
            return