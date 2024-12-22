"""Graphical game"""

from modules.rolit import *
from time import sleep
from time import ctime
import os
import os.path
import modules.fltk as fltk
import modules.fltk_addons as addons
import modules.saver as saver

# graphical display variables
GRID = 830 # ui elements width
SIDE = 330
QUARTER = (GRID+SIDE)/4
PADDING = 20
BASE_BAR_X = 860 # base coordinates for the score bars
BASE_BAR_Y = 100
BAR_HEIGHT = 50 # height of the score bars
BAR_VERTICAL_SPACING = 10 # spacing between score bars
MAX_BAR_WIDTH = SIDE-40
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

ALL_COLORS = [
    {   #Base
        CLEAR: "#AED2FF",
        RED: "#FF004D",
        GREEN: "#00DFA2",
        YELLOW: "#FAEF5D",
        BLUE: "#0079FF"
    },
    {   #Dracula
        CLEAR: "#F8F8F2",
        RED: "#FF5555",
        GREEN: "#BD93F9", #Purple
        YELLOW: "#F1FA8C",
        BLUE: "#FF79C6" #Pink
    },
    {   #Nord
        CLEAR: "#d8dee9",
        RED: "#FF5555",
        GREEN: "#a3be8c",
        YELLOW: "#ebcb8b",
        BLUE: "#5e81ac"
    },
    {   #Tropical mdr
        CLEAR: "#a5c5c2",
        RED: "#e12729",
        GREEN: "#72b043",
        YELLOW: "#ffb629",
        BLUE: "#75c9e3"
    },
    {   #Protanopia
        CLEAR: "#dddffd",
        RED: "#867f6e",
        GREEN: "#d1c395",
        YELLOW: "#ffea94",
        BLUE: "#0079fc"
    },
    {   #Deuteranopia
        CLEAR: "#e7dcff",
        RED: "#9f793f",
        GREEN: "#dfbcac",
        YELLOW: "#ffe6ca",
        BLUE: "#0080da"
    },
    {   #Tritanopia
        CLEAR: "#cce5f7",
        RED: "#fe201b",
        GREEN: "#4fd5e6",
        YELLOW: "#ffe3ee",
        BLUE: "#008b93"
    },
]
COLORS_LIST = ["CLEAR","RED","YELLOW","GREEN","BLUE"]
COLOR_INDEX = 0
SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

TURNS = {
    1: [RED],
    2: [RED, GREEN],
    3: [RED, YELLOW, GREEN],
    4: [RED, YELLOW, GREEN, BLUE]
}

DESC = "Le but du jeu est d'avoir\nle plus de boule de sa\ncouleur sur le plateau.\n\nLe jeu se joue en manches.\n\nLe gagnant est le joueur\nqui a gagné le plus de\nmanches !"
RULES = """Début de partie:
    - Chaque joueur choisit une couleur
    - Une boule de chaque couleur est placée au
    centre du plateau
    - Le joueur qui commence est choisi
    aléatoirement
Déroulement d'un tour:
    - Le joueur doit placer une boule de sa couleur
    adjacente à une boule déjà présente
    - Les boules adverses prises en "sandwich" entre
    une boule venant d'être placée et une boule de
    la couleur du joueur sont dites "capturées" et
    deviennent de la couleur du joueur
Fin d'une manche:
    - La manche se termine lorsque le plateau est
    plein
    - Le joueur ayant le plus de boules de sa
    couleur gagne la manche
    - En cas d'égalité, les joueurs concernés
    gagnent la manche
Fin de la partie:
    - La partie se termine après un nombre de
    manches défini préalablement
    - Le joueur ayant gagné le plus de manches
    remporte la partie
    - En cas d'égalité, les joueurs concernés
    gagnent la partie
"""

addons.init(fltk) # initialize the fltk_addons module
if not os.path.exists("saves"): # create the saves directory if it doesn't exist
    os.makedirs("saves")

def display_grid_window(grid: list[list[int]], player: int, current_round: int, scores: list[list[int]] | None = None) -> None:
    """Display the game grid onto the fltk window and side informations
    
    :param grid: game grid
    :param player: the current player
    :param current_round: the current round
    :param scores: scores of the players by round"""
    fltk.efface_tout()
    # draw black background with an outline set as the current player's color
    fltk.rectangle(0,0,830,830, couleur=SELECTED_COLORS[player], remplissage="#222831", epaisseur=30)
    for i_row in range(len(grid)):
        for i_elem in range(len(grid[0])):
            # for each element of the game grid, draw circle of according color
            if grid[i_row][i_elem] == CLEAR and not test_adjacent(grid, i_elem, i_row): # If slot is unused and unreachable, fill in gray
                fltk.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, "#393E46", remplissage="#393E46")
            else: # Else, look in color lookup table
                fltk.cercle(100*i_elem + 50 + 15, 100*i_row + 50 + 15, 40, SELECTED_COLORS[grid[i_row][i_elem]], remplissage=SELECTED_COLORS[grid[i_row][i_elem]])
    # Re draw background for side view
    fltk.rectangle(GRID, 0, GRID+SIDE, GRID, couleur="#F0F0F0", remplissage="#F0F0F0")

    # Draw the outline of the side view
    fltk.rectangle(GRID+PADDING, 20, GRID+SIDE, 810, epaisseur=5)
    # Settings icon
    fltk.texte(GRID+SIDE-40/2-20, GRID-40/2-10, chaine="⚙️", taille=40, ancrage="s", tag="settings-icon")

    # Affichage du header "Scores"
    fltk.texte(GRID+(PADDING+SIDE)/2, 50, chaine="Scores", ancrage="center", police="Cascadia Code", taille=25)
    if scores[current_round]:
        current_scores = scores[current_round]
        max_score = max(current_scores)
        for i in range(4):
            bar_y = BASE_BAR_Y + (BAR_HEIGHT + BAR_VERTICAL_SPACING) * i # calculate the y coordinate of the bar
            bar_width = max((current_scores[i] / max_score)*MAX_BAR_WIDTH, 40) # calculate the width of the bar
            fltk.rectangle(BASE_BAR_X, bar_y, BASE_BAR_X + bar_width, bar_y + BAR_HEIGHT, epaisseur=5, remplissage=SELECTED_COLORS[i+1])
            fltk.texte(BASE_BAR_X+10, bar_y, str(current_scores[i]), ancrage="nw", police="Cascadia Code", taille=25)
            if current_scores[i] == max_score and max_score != 0:
                fltk.texte(BASE_BAR_X+MAX_BAR_WIDTH-60, bar_y, "👑", couleur="#FFAF4D", ancrage="nw", police="Cascadia Code", taille=25) # add a crown for the leading player

    fltk.texte(GRID+(PADDING+SIDE)/2, 400, chaine="Manches gagnées", ancrage="center", police="Cascadia Code", taille=25) # display the total score
    if scores:
        rounds_won = [sum(scores[round_id][player_id] == max(scores[round_id]) for round_id in range(current_round)) for player_id in range(4)]
        for i in range(4):
            bar_y = 450 + (BAR_HEIGHT + BAR_VERTICAL_SPACING) * i # calculate the y coordinate of the bar
            bar_width = max((rounds_won[i] / max(*rounds_won, 1))*MAX_BAR_WIDTH, 40) # calculate the width of the bar
            fltk.rectangle(BASE_BAR_X, bar_y, BASE_BAR_X + bar_width, bar_y + BAR_HEIGHT, epaisseur=5, remplissage=SELECTED_COLORS[i+1])
            fltk.texte(BASE_BAR_X+10, bar_y, str(rounds_won[i]), ancrage="nw", police="Cascadia Code", taille=25)
            if rounds_won[i] == max(rounds_won) and rounds_won[i] != 0:
                fltk.texte(BASE_BAR_X+MAX_BAR_WIDTH-60, bar_y, "👑", couleur="#FFAF4D", ancrage="nw", police="Cascadia Code", taille=25) # add a crown for the leading player

def display_end_window(scores: list[int], text: str) -> None:
    """Display the end window with the final scores

    :param scores: the final scores of each player
    :param text: the text to display in the side view"""
    fltk.efface_tout()
    fltk.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[RED])
    fltk.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[YELLOW])
    fltk.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[BLUE])
    fltk.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[GREEN])

    for i in range(4):
        if scores[i] == max(scores):
            crown_x = 415/2 + (415 * (i in (1, 2)))
            crown_y = 415/2 - 50 + (415 * (i in (2, 3)))
            fltk.texte(crown_x, crown_y, "👑", couleur="#FFAF4D", ancrage="center", police="Cascadia Code", taille=200)

    fltk.texte(207, 207, str(scores[0]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(622, 207, str(scores[1]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(207, 622, str(scores[3]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(622, 622, str(scores[2]), ancrage="center", police="Cascadia Code", taille=128)

    fltk.texte(GRID+(PADDING+SIDE)/2, 50, chaine=text, couleur="black", ancrage="n", police="Cascadia Code", taille=25)

    ev = None
    while True:
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        if ev is None: continue
        if ev[0] == "ClicGauche":
            return
        elif ev[0] == "Quitte":
            return -1


def menu_window_select(texts: tuple[str, str, str, str]) -> int:
    """Display a window with 4 choices and return the selected one
    
    :param texts: the texts to display on the window
    :return: the selected choice (1-4)"""
    fltk.efface_tout()
    fltk.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[RED])
    fltk.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[YELLOW])
    fltk.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[BLUE])
    fltk.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[GREEN])

    fltk.texte(207, 207, texts[0], ancrage="center", police="Cascadia Code", taille=48)
    fltk.texte(622, 207, texts[1], ancrage="center", police="Cascadia Code", taille=48)
    fltk.texte(207, 622, texts[2], ancrage="center", police="Cascadia Code", taille=48)
    fltk.texte(622, 622, texts[3], ancrage="center", police="Cascadia Code", taille=48)

    fltk.texte(GRID+(PADDING+SIDE)/2, 50, chaine="Rolit", couleur="black", ancrage="center", police="Cascadia Code", taille=25)
    fltk.texte(GRID+(PADDING+SIDE)/2, 80, chaine=DESC, couleur="black", ancrage="n", police="Cascadia Code", taille=16)
    fltk.texte(GRID+(PADDING+SIDE)/2, 400, chaine="A vos boules !", couleur="black", ancrage="center", police="Cascadia Code", taille=25)

    if len(saves) > 0:
        date = ctime(os.path.getmtime(saves[0])).split() #Get latest date and convert from Unix to readable - [1] to take the date and not the true/false return, 0 to take the soonest file
        fltk.rectangle(GRID+PADDING, GRID-160, GRID+SIDE, GRID-70, epaisseur=5, remplissage="#F0F0F0", tag="recall")
        fltk.texte(GRID+(PADDING+SIDE)/2, 700, "Reprendre", ancrage="center", police="Cascadia Code", taille=30, tag="recall")
        fltk.texte(GRID+(PADDING+SIDE)/2, 735, (date[2]+"/"+str(MONTHS[date[1]])+" "+date[3]), ancrage="center", police="Cascadia Code", taille=12, tag="recall")
        fltk.rectangle(GRID+(PADDING+SIDE)/2-100, 780, GRID+(PADDING+SIDE)/2+100, 810, epaisseur=3, remplissage="#F0F0F0", tag="select-save")
        fltk.texte(GRID+(PADDING+SIDE)/2, 795, "Choisir sauvegarde", ancrage="center", police="Cascadia Code", taille=12, tag="select-save")

    ev = None
    while True:
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        if ev is None: continue
        if ev[0] == "ClicGauche":
            if ev[1].x <= 830:
                if ev[1].x <= 415 and ev[1].y <= 415:
                    return 1
                if ev[1].x >= 415 and ev[1].y <= 415:
                    return 2
                if ev[1].x <= 415 and ev[1].y >= 415:
                    return 3
                if ev[1].x >= 415 and ev[1].y >= 415:
                    return 4
            elif addons.est_objet_survole("recall"):
                return 5
            elif addons.est_objet_survole("select-save"):
                save = save_menu(saves)
                if save == -2:
                    return -2
                elif save == -1:
                    return -1   #Car -1 déjà pris dans les valeurs de mainloop
                else:
                    return save   #select_save acivé
        elif ev[0] == "Quitte":
            return -1


def submenu_title(x1: int, y1: int, x2: int, y2: int, text: str = "Submenu") -> None:
    """Display a submenu title
    
    :param x1: the x coordinate of the top left corner
    :param y1: the y coordinate of the top left corner
    :param x2: the x coordinate of the bottom right corner
    :param y2: the y coordinate of the bottom right corner
    :param text: the text to display"""
    fltk.rectangle(x1, y1, x2, y2, epaisseur=5)
    fltk.texte((x1+x2)/2, (y1+y2)/2, text, ancrage="center", police="Cascadia Code", taille=25)


def theme_btn(i: int) -> int:
    """Display a button for a theme

    :param i: the index of the theme
    :return: the id of the button"""
    start_x = 2*QUARTER + PADDING
    end_x = 3*QUARTER - PADDING
    out = fltk.rectangle(start_x, 130 + i*60, end_x, 180 + i*60, epaisseur=5, remplissage="#123456")
    for j in range(5):
        fltk.rectangle(
            ax = (start_x + 2.5) + j*(end_x - start_x - 5)/5,
            ay = 130 + i*60 + 2.5,
            bx = (start_x + 2.5) + (j + 1)*(end_x - start_x - 5)/5,
            by = 180 + i*60 - 2.5,
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


def draw_save_btns() -> None:
    start_x = 3*QUARTER + PADDING
    end_x = 4*QUARTER - PADDING
    fltk.rectangle(start_x, 130, end_x, 180, epaisseur=5, remplissage="#F0F0F0", tag="save")
    fltk.texte((start_x+end_x)//2, 155, "Sauvegarder", ancrage="center", police="Cascadia Code", taille=17, tag="save")
    if len(saves) > 0:
        fltk.rectangle(start_x, 190, end_x, 240, epaisseur=5, remplissage="#F0F0F0", tag="recall")
        fltk.texte((start_x+end_x)//2, 215, "Charger sauvegarde", ancrage="center", police="Cascadia Code", taille=17, tag="recall")


def settings_menu() -> tuple[str, int]:
    """Display the settings menu
    
    :return: the selected option"""
    fltk.efface_tout()
    submenu_title(PADDING-10, 40, 2*QUARTER-PADDING+10, 100, "Règles")
    submenu_title(2*QUARTER+PADDING-10, 40, 3*QUARTER-PADDING+10, 100, "Thèmes")
    submenu_title(3*QUARTER+PADDING-10, 40, 4*QUARTER-PADDING+10, 100, "Sauvegarde")
    theme_boxes = themes()

    fltk.texte(10, 130, chaine=RULES, ancrage="nw", police="Cascadia Code", taille=14)
    draw_save_btns() # save btns
    # back button
    fltk.texte(GRID+SIDE-40/2-10, GRID-40/2-10, "🔙", ancrage="s", police="Cascadia Code", taille=40, tag="back")

    while True:
        ev = fltk.donne_ev()
        if addons.est_objet_survole("back"):
            fltk.cercle(GRID+SIDE-40/2-10, GRID-40/2-38, 38, couleur="black", epaisseur=2, tag="hover-back")
        else:
            fltk.efface("hover-back")

        if ev != None:
            match ev[0]:
                case "Quitte":
                    return ("quit", -1)
                case "Touche":
                    if ev[1].keysym == "Escape":
                        return ("back", None)
                case "ClicGauche":
                    for i in range(len(theme_boxes)):
                        if addons.est_objet_survole(theme_boxes[i]):
                            return ("theme", i)
                    if addons.est_objet_survole("save"):
                        return ("save", None)
                    if addons.est_objet_survole("recall"):
                        return ("recall", None)
                    if addons.est_objet_survole("back"):
                        return ("back", None)
            ev = fltk.donne_ev()
        fltk.mise_a_jour()


def mainloop(nb_players: int, nb_rounds: int, ai: bool) -> None:
    """Main game loop

    :param nb_players: number of players
    :param nb_rounds: number of rounds
    :param ai: if the player wants to play against the AI"""
    global ALL_COLORS, COLOR_INDEX, SELECTED_COLORS, saves
    saves = saves_list()
    # create the game window
    fltk.cree_fenetre(GRID+PADDING+SIDE, GRID, 60, False)
    addons.renomme_fenetre("Rolit")

    ok = False # if all choices are done
    skip = False # wether to skip round initialization (only to be set to True when recalling a game)
    select_save = False

    while not ok:
        if nb_players == 0: # if the player didn't choose the number of players, select the number of players
            choice = menu_window_select(("1 Joueur", "2 Joueurs", "3 Joueurs", "4 Joueurs"))
            while choice == -2:
                choice = menu_window_select(("1 Joueur", "2 Joueurs", "3 Joueurs", "4 Joueurs"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if isinstance(choice, str): #Si c'est une save renvoyée
                select_save = True
                break
            nb_players = choice
        if nb_players != 0: # when player number is selected, select ai number
            choice = menu_window_select(("Aucune IA", "1 IA", "2 IA", "3 IA"))
            while choice == -2:
                choice = menu_window_select(("Aucune IA", "1 IA", "2 IA", "3 IA"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if isinstance(choice, str):
                select_save = True
                break
            if (choice-1) + nb_players > 4:
                continue
            nb_ai = choice - 1
            ai = True
        if nb_rounds == 0: # if the player didn't choose the number of rounds, select the number of rounds
            choice = menu_window_select(("1 Manche", "2 Manches", "3 Manches", "4 Manches"))
            while choice == -2:
                choice = menu_window_select(("1 Manche", "2 Manches", "3 Manches", "4 Manches"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if isinstance(choice, str):
                select_save = True
                break
            nb_rounds = choice
        ok = True

    round_i = 0
        
    scores = [[None] * 4 for _ in range(nb_rounds)]
    
    if skip:
        gameState = saver.recall(saves[0])
        grid, player_bias, tour, nb_players, nb_ai, nb_rounds, round_i, scores, COLOR_INDEX = gameState
        SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

    if select_save:
        gameState = saver.recall(choice)
        grid, player_bias, tour, nb_players, nb_ai, nb_rounds, round_i, scores, COLOR_INDEX = gameState
        SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

    while round_i < nb_rounds:
        if not skip and not select_save:
            player_bias = randint(0, 4)
            grid = init_grid()
            tour = 0
        skip = False
        while tour < 60:
            # simple formula to get player index based on the number of players and the index of the turn
            player = (tour + player_bias) % (nb_players + nb_ai) + 1
            player = TURNS[nb_players + nb_ai][player - 1]
            scores[round_i] = calc_score(grid)
            display_grid_window(grid, player, round_i, scores)
            # loop over events
            ev = fltk.donne_ev()
            if addons.est_objet_survole("settings-icon"):
                fltk.cercle(GRID+SIDE-40/2-20, GRID-40/2-10-32, 32, couleur="black", epaisseur=2)

            while ev != None:
                match ev[0]:
                    case "Quitte":
                        # Pretty straightforward
                        fltk.ferme_fenetre()
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
                                scores[round_i] = calc_score(grid)
                                display_grid_window(grid, player, round_i, scores)
                                fltk.mise_a_jour()
                                sleep(1)
                                for _ in range(nb_ai):
                                    # get current IA player id
                                    player = (tour + player_bias) % (nb_players + nb_ai) + 1
                                    player = TURNS[nb_players + nb_ai][player - 1]
                                    # make them play
                                    ai_play(grid, player)
                                    tour += 1
                                    # between each IA turn, display and wait
                                    scores[round_i] = calc_score(grid)
                                    display_grid_window(grid, player, round_i, scores)
                                    fltk.mise_a_jour()
                                    fltk.__canevas.ev_queue.clear()
                                    sleep(1)
                        elif addons.est_objet_survole("settings-icon"):
                            draw_save_btns()
                            param_out = settings_menu()
                            match param_out[0]:
                                case "quit":
                                    fltk.ferme_fenetre()
                                    return
                                case "theme":
                                    COLOR_INDEX = param_out[1]
                                    SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]
                                case "save":
                                    fltk.efface_tout() #Affichage de la page blanche avec l'input box pour le nom du fichier auquel on rajoutera .save
                                    fltk.texte((GRID+SIDE)/2, GRID/3-10, "Nom du fichier de sauvegarde", ancrage="s", police="Cascadia Code", taille=25, tag="box-input")
                                    fltk.rectangle((GRID+SIDE)/3, GRID/3, 2*(GRID+SIDE)/3, 2*GRID/5, couleur="black", epaisseur=2, tag="box-input")
                                    savename = name_input((GRID+SIDE)/3+20, GRID/3+30, "w")
                                    if savename == -2:
                                        continue
                                    elif savename == -1:
                                        fltk.ferme_fenetre()
                                        return
                                    else:
                                        saver.save("saves/"+savename+".save", grid, player_bias, nb_players, nb_ai, nb_rounds, round_i, scores, COLOR_INDEX)
                                        saves = saves_list()
                                case "recall":
                                    saves = saves_list() # Mise à jour des saves du dossier
                                    save = save_menu(saves)
                                    if save == -2:
                                        continue
                                    elif save == -1:
                                        fltk.ferme_fenetre()
                                        return
                                    else:
                                        gameState = saver.recall(save)
                                        grid, player_bias, tour, nb_players, nb_ai, nb_rounds, round_i, scores, COLOR_INDEX = gameState
                                        SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

                    case "Touche":
                        pass
                        # Do whatever debug shit here

                # grab next event
                ev = fltk.donne_ev()
            # update the window after event handling
            fltk.mise_a_jour()

        # after the game has ended, calculate the score and print it
        scores[round_i] = calc_score(grid)

        if display_end_window(scores[round_i], "Score de fin\nde manche") == -1:
            fltk.ferme_fenetre()
            return

        round_i += 1
    
    if nb_rounds != 1:
        scores_finaux = [sum(scores[round_id][player_id] == max(scores[round_id]) for round_id in range(nb_rounds)) for player_id in range(4)]
        display_end_window(scores_finaux, "Fin de partie\nScore final")


def saves_list() -> tuple[bool, list[str]]:
    """Returns the list of all save files name
    
    :return: The list of saves"""
    list = os.listdir("saves/")
    saves = []

    for el in list:
        if len(el) > 4:
            if el.endswith("save"):
                saves.append(f"saves/{el}")

    if saves != []:
        saves.sort(reverse=True, key = lambda x: os.path.getmtime(x))
        return saves
    
    return []


def name_input(x: int, y: int, anchor: str) -> str:
    """Input handler for the save file name.
    
    :param x: x coordinate of the input box
    :param y: y coordinate of the input box
    :param anchor: anchor point"""
    name = ""
    confirm = False

    fltk.efface("input")
    while not confirm:
        evName, event = fltk.attend_ev() #Get event
        match evName:
            case "Touche":
                key = event.keysym
                text = event.char
                if key == "Escape":
                    return -2
                elif len(name) >= 22:
                    fltk.efface("input")
                    fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor, couleur="red")
                    name = name[:-1]
                else:
                    fltk.efface("input")
                    if key=="Return":
                        return name
                    elif key =="BackSpace":
                        if name !="":
                            name=name[:-1]
                            fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor) 
                    elif not text:
                        fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor)
                        continue
                    else:
                        name += text
                        fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor)
            case "Quitte":
                return -1

def save_menu(saves: list[str], xsaves: list[str] | None = None) -> str:
    """Menu for choosing, searching and deleting save files.
    
    :param saves: saves that are right now in the folder
    :param xsaves: saves with search filter applied, also = saves if no saves are in the search results
    :param anchor: anchor point"""
    confirm = False
    fltk.efface_tout()
    fltk.texte((GRID+SIDE)/2, GRID/8, "Rechercher :", ancrage="s", police="Cascadia Code", taille=25, tag="box-input")
    fltk.rectangle((GRID+SIDE)/3, GRID/6, 2*(GRID+SIDE)/3, 2*GRID/8, couleur="#d8dee9", epaisseur=3, remplissage="white", tag="box-input")
    # Si la liste secondaire est vite, on prend la main, sinon on prend celle-ci
    if xsaves == None or len(xsaves)==0:
        xsaves = saves

    for i in range(min(len(xsaves), 5)): # On affiche uniquement les 5 premiers résultats (len(xsaves) si < 5 sinon 5)
        date = ctime(os.path.getmtime(xsaves[i])).split()
        fltk.rectangle(3*(GRID+SIDE)/14, (6+3/2*i)*GRID/14, 11*(GRID+SIDE)/14, (7+3/2*i)*GRID/14, couleur="black", epaisseur=3, tag=xsaves[i])
        fltk.texte((GRID+SIDE)/2, (6+3/2*i)*GRID/14+30, (xsaves[i])[:-5]+" - "+(date[2]+"/"+str(MONTHS[date[1]])+" "+date[3]), ancrage="center", tag=xsaves[i])
        fltk.texte(5*(GRID+SIDE)/6, (6+3/2*i)*GRID/14+10, "🗑️", tag=xsaves[i]+"bin")
        fltk.mise_a_jour()

    while not confirm:
        evName, event = fltk.attend_ev() #Get event
        match evName:
            case "ClicGauche":
                survol = addons.objet_survole()
                if survol != None:
                    cible = addons.recuperer_tags(survol)[0]
                    #Si le survol finit par save, c'est la save cible et donc on la renvoie pour la charger
                    if cible[-4:] == "save":
                        return cible
                    #Si le survol finit par bin, on supprime le fichier et // on réactualise la liste
                    if cible[-3:] == "bin":
                        os.remove(cible[:-3])
                        xsaves = xsaves.remove(cible[:-3])
                        newsave = save_menu(saves, xsaves)
                        saves = saves_list() # Mise à jour des saves dans le dossier
                        return newsave

                    if cible == "box-input":
                        fltk.efface_tout()
                        fltk.texte((GRID+SIDE)/2, GRID/8, "Rechercher :", ancrage="s", police="Cascadia Code", taille=25, tag="box-input")
                        fltk.rectangle((GRID+SIDE)/3, GRID/6, 2*(GRID+SIDE)/3, 2*GRID/8, couleur="black", epaisseur=3, remplissage="white", tag="box-input")
                        #On prend la recherche du user
                        search = name_input((GRID+SIDE)/3+20, GRID/6+30, "w")
                        if search == -1:
                            return -1
                        elif search != -2:
                            #On crée une liste secondaire ne contenant que les saves contenant l'input
                            xsaves = [el for el in xsaves if search in el[:-5]]
                            #On imbrique la fonction
                        newsave = save_menu(saves, xsaves)
                        return newsave
            case "Touche":
                key = fltk.touche((evName, event))
                if key == "Escape":
                    return -2
            case "Quitte":
                return -1
