"""Graphical game"""

from modules.rolit import *
from time import sleep
import modules.fltk as fltk
import modules.fltk_addons as addons
import modules.saver as saver
from os.path import isfile, getmtime
from os import listdir
from time import ctime

addons.init(fltk)

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
    }
]
COLORS_LIST = ["CLEAR","RED","YELLOW","GREEN","BLUE"]
COLOR_INDEX = 0
SELECTED_COLORS = ALL_COLORS[COLOR_INDEX]

def display_grid_window(grid: list[list[int]], player: int | None = None, current_scores: list[int] | None = None) -> None:
    """Display the game grid onto the fltk window and side informations
    
    :param grid: game grid
    :param player: the current player
    :param current_scores: the current scores of each player"""
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

    # Draw the score header outline
    fltk.rectangle(BASE_BAR_X-10, 20, BASE_BAR_X+MAX_BAR_WIDTH+10, 810, epaisseur=5)
    # Affichage du header "Scores"
    fltk.texte(GRID+SIDE/2+10,50,chaine="Scores", ancrage="center", police="Cascadia Code", taille=25)
    fltk.texte(GRID+SIDE+(SETTINGS-55)/2+25, 20, chaine="⚙️", taille=40, ancrage="n", tag="settings-icon")
    # fltk.image(GRID+SIDE+(SETTINGS-55)/2, 20, fichier="assets/settings.png", largeur=55, hauteur=55, ancrage="nw", tag="settings-icon")

    if current_scores:
        max_score = max(current_scores)
        for i in range(max(len(current_scores), 4)):
            bar_y = BASE_BAR_Y + (BAR_HEIGHT + BAR_VERTICAL_SPACING) * i # calculate the y coordinate of the bar
            bar_width = max((current_scores[i] / max_score)*MAX_BAR_WIDTH, 40) # calculate the width of the bar
            fltk.rectangle(BASE_BAR_X, bar_y, BASE_BAR_X + bar_width, bar_y + BAR_HEIGHT, epaisseur=5, remplissage=SELECTED_COLORS[i+1])
            fltk.texte(BASE_BAR_X+10, bar_y, str(current_scores[i]), ancrage="nw", police="Cascadia Code", taille=25)
            if current_scores[i] == max_score:
                fltk.texte(BASE_BAR_X+MAX_BAR_WIDTH-60, bar_y, "👑", couleur="#FFAF4D", ancrage="nw", police="Cascadia Code", taille=25) # add a crown for the leading player
                # fltk.image(BASE_BAR_X+MAX_BAR_WIDTH-60, bar_y, "assets/crown_perfect_size.png", largeur=50, hauteur=50, ancrage="nw") # add a crown for the leading player


def display_end_window(scores: list[int]) -> None:
    """Display the end window with the final scores

    :param scores: the final scores of each player"""
    fltk.efface_tout()
    fltk.rectangle(-5, -5, 415, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[RED])
    fltk.rectangle(415, -5, 835, 415, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[YELLOW])
    fltk.rectangle(-5, 415, 415, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[BLUE])
    fltk.rectangle(415, 415, 835, 835, couleur="black", epaisseur=5, remplissage=SELECTED_COLORS[GREEN])

    crown_x = 415/2 + 415 * (max(scores) == scores[1] or max(scores) == scores[3]) # calculate the coordinates of the crown
    crown_y = 415/2 - 50 + 415 * (max(scores) == scores[2] or max(scores) == scores[3])
    # crown_x = 415 * (max(scores) == scores[1] or max(scores) == scores[3]) # crown coordinates (image)
    # crown_y = 415 * (max(scores) == scores[2] or max(scores) == scores[3])

    fltk.PIL_AVAILABLE = False
    fltk.texte(crown_x, crown_y, "👑", couleur="#FFAF4D", ancrage="center", police="Cascadia Code", taille=200)
    # fltk.image(crown_x, crown_y, "assets/crown_perfect_size.png", largeur=415, hauteur=415, ancrage="nw")

    fltk.texte(207, 207, str(scores[0]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(622, 207, str(scores[1]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(207, 622, str(scores[2]), ancrage="center", police="Cascadia Code", taille=128)
    fltk.texte(622, 622, str(scores[3]), ancrage="center", police="Cascadia Code", taille=128)

    fltk.texte(1060,50,chaine="<Félicitations ?> ", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)
    fltk.texte(1060,80,chaine="<Scores de manches ?>", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)

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

    fltk.texte(1060,50,chaine="<Règles ?> ", couleur="#393E46", ancrage="center", police="Cascadia Code", taille=25)

    #if isfile("rolit.save"):
    saves = saves_list()
    if len(saves) > 0:
        date = ctime(getmtime(saves[0])).split() #Get latest date and convert from Unix to readable - [1] to take the date and not the true/false return, 0 to take the soonest file
        fltk.rectangle(880, 650, 1190, 750, epaisseur=5, remplissage="#F0F0F0", tag="recall")
        fltk.texte(1035, 700, "Reprendre", ancrage="center", police="Cascadia Code", taille=30, tag="recall")
        fltk.texte(1035, 735, (date[2]+"/"+str(MONTHS[date[1]])+" "+date[3]), ancrage="center", police="Cascadia Code", taille=12, tag="recall")
        fltk.rectangle(942, 780, 1128, 810, epaisseur=3, remplissage="#F0F0F0", tag="select-save")
        fltk.texte(1035, 795, "Choisir sauvegarde", ancrage="center", police="Cascadia Code", taille=12, tag="select-save")

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
                return 6
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
    out = fltk.rectangle(start_x, 150 + i*70, end_x, 200 + i*70, epaisseur=5, remplissage="#123456")
    for j in range(5):
        fltk.rectangle(
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


def draw_save_btns() -> None:
    start_x = 3*QUARTER + PADDING
    end_x = 4*QUARTER - PADDING
    fltk.rectangle(start_x, 150, end_x, 200, epaisseur=5, remplissage="#F0F0F0", tag="save")
    fltk.texte((start_x+end_x)//2, 175, "Sauvegarder", ancrage="center", police="Cascadia Code", taille=17, tag="save")
    if isfile("rolit.save"):
        fltk.rectangle(start_x, 220, end_x, 270, epaisseur=5, remplissage="#F0F0F0", tag="recall")
        fltk.texte((start_x+end_x)//2, 245, "Charger sauvegarde", ancrage="center", police="Cascadia Code", taille=17, tag="recall")


def settings_menu() -> tuple[str, int]:
    """Display the settings menu
    
    :return: the selected option"""
    fltk.efface_tout()
    submenu_title(PADDING-10, 40, 2*QUARTER-PADDING+10, 100, "Règles")
    submenu_title(2*QUARTER+PADDING-10, 40, 3*QUARTER-PADDING+10, 100, "Thèmes")
    #submenu_title(2*QUARTER+PADDING-10, 40, 3*QUARTER-PADDING+10, 100, "Accessibilité")
    submenu_title(3*QUARTER+PADDING-10, 40, 4*QUARTER-PADDING+10, 100, "Sauvegarde")
    theme_boxes = themes()
    
    draw_save_btns() # save btns
    # back button
    fltk.texte(GRID+SIDE+(SETTINGS-55)/2+25, 750, "🔙", ancrage="n", police="Cascadia Code", taille=40, tag="back")
    
    while True:
        ev = fltk.donne_ev()
        if addons.est_objet_survole("back"):
            fltk.cercle(GRID+SIDE+(SETTINGS-55)/2+25, 790, 38, couleur="black", epaisseur=2, tag="hover-back")
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
                            fltk.rectangle(QUARTER+PADDING, 150 + i*70, 2*QUARTER-PADDING, 200 + i*70, epaisseur=8, couleur=ALL_COLORS[i][GREEN])
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
    global ALL_COLORS, COLOR_INDEX, SELECTED_COLORS
    saves = saves_list()
    # create the game window
    fltk.cree_fenetre(GRID+SIDE+SETTINGS, GRID, 60, False)
    addons.renomme_fenetre("Rolit")

    ok = False # if all choices are done
    skip = False # wether to skip round initialization (only to be set to True when recalling a game)
    select_save = False

    while not ok:
        if nb_players == 0: # if the player didn't choose the number of players, select the number of players
            choice = menu_window_select(("1 Joueur", "2 Joueurs", "3 Joueurs", "4 Joueurs"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if choice == 6:
                select_save = True
                break
            nb_players = choice
        if nb_players != 0: # when player number is selected, select ai number
            choice = menu_window_select(("Aucune IA", "1 IA", "2 IA", "3 IA"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if choice == 6:
                select_save = True
                break
            if (choice-1) + nb_players > 4:
                continue
            nb_ai = choice - 1
            ai = True
        if nb_rounds == 0: # if the player didn't choose the number of rounds, select the number of rounds
            choice = menu_window_select(("1 Manche", "2 Manches", "3 Manches", "4 Manches"))
            if choice == -1:
                return
            if choice == 5:
                skip = True
                break
            if choice == 6:
                select_save = True
                break
            nb_rounds = choice
        ok = True

    round_i = 0
        
    if skip:
        gameState = saver.recall(saves[0])
        grid, player_bias, tour, nb_players, nb_ai = gameState
        nb_rounds = 1

    if select_save:
        gameState = saver.recall(save_menu(saves))
        grid, player_bias, tour, nb_players, nb_ai = gameState
        
    scores = [[None] * 4 for _ in range(nb_rounds)]

    while round_i < nb_rounds:
        if not skip:
            player_bias = randint(0, 4)
            grid = init_grid()
            tour = 0
        skip = False
        while tour < 60:
            # simple formula to get player index based on the number of players and the index of the turn
            player = (tour + player_bias) % (nb_players + nb_ai) + 1
            display_grid_window(grid, player, calc_score(grid))
            # loop over events
            ev = fltk.donne_ev()
            if addons.est_objet_survole("settings-icon"):
                fltk.cercle(GRID+SIDE+(SETTINGS-55)/2+25, 48, 32, couleur="black", epaisseur=2)

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
                                display_grid_window(grid, player, calc_score(grid))
                                fltk.mise_a_jour()
                                sleep(1)
                                for _ in range(nb_ai):
                                    # get current IA player id
                                    player = (tour + player_bias) % (nb_players + nb_ai) + 1
                                    # make them play
                                    ai_play(grid, player)
                                    tour += 1
                                    # between each IA turn, display and wait
                                    display_grid_window(grid, player, calc_score(grid))
                                    fltk.mise_a_jour()
                                    fltk.__canevas.ev_queue.clear()
                                    sleep(1)
                        elif addons.est_objet_survole("settings-icon"):
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
                                    fltk.texte((GRID+SIDE+SETTINGS)/2, GRID/3-10, "Nom du fichier de sauvegarde", ancrage="s", police="Cascadia Code", taille=25, tag="box-input")
                                    fltk.rectangle((GRID+SIDE+SETTINGS)/3, GRID/3, 2*(GRID+SIDE+SETTINGS)/3, 2*GRID/5, couleur="black", epaisseur=2, tag="box-input")
                                    savename = name_input((GRID+SIDE+SETTINGS)/3+20, GRID/3+30, "w")
                                    saver.save(savename+".save", grid, player_bias, nb_players, nb_ai, nb_rounds, round_i)
                                case "recall":
                                    gameState = saver.recall(saves_list()[1][0])
                                    grid, player_bias, tour, nb_players, nb_ai = gameState

                    case "Touche":
                        pass
                        # Do whatever debug shit here

                # grab next event
                ev = fltk.donne_ev()
            # update the window after event handling
            fltk.mise_a_jour()

        # after the game has ended, calculate the score and print it
        scores[round_i] = calc_score(grid)
        
        print(COLOR_NAMES[scores[round_i].index(max(scores[round_i]))+1])

        if display_end_window(scores[round_i]) == -1:
            fltk.ferme_fenetre()
            return
        
        round_i += 1
    
    if nb_rounds != 1:
        scores_finaux = [sum(scores[round_id][player_id] for round_id in range(nb_rounds)) for player_id in range(4)]
        display_end_window(scores_finaux)


def saves_list() -> tuple[bool, list[str]]:
    """Returns the list of all save files name
    
    :return: The list of saves"""
    list = listdir()
    saves = []

    for el in list:
        if len(el) > 4:
            if el.endswith("save"):
                saves.append(el)

    if saves != []:
        saves.sort(reverse=True, key = lambda x: getmtime(x))
        return saves
    
    return []


def name_input(x: int, y: int, anchor: str) -> str:
    """Input handler for the save file name
    
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
                if len(name) >= 22:
                    fltk.efface("input")
                    fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor, couleur="red")
                    name = name[:-1]
                else:
                    fltk.efface("input")
                    key = fltk.touche((evName, event))
                    if key=="Return":
                        return name
                    elif key =="BackSpace":
                        if name !="":
                            name=name[:-1]
                            fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor) 
                    elif len(key) > 2:
                        fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor)
                        continue
                    else:
                        name += key
                        fltk.texte(x, y, str(name), police="Cascadia Code", tag="input", ancrage=anchor)
            case "Quitte":
                fltk.ferme_fenetre()

def save_menu(saves):

    confirm = False
    fltk.efface_tout()
    fltk.texte((GRID+SIDE+SETTINGS)/2, GRID/8, "Rechercher :", ancrage="s", police="Cascadia Code", taille=25, tag="box-input")
    fltk.rectangle((GRID+SIDE+SETTINGS)/3, GRID/6, 2*(GRID+SIDE+SETTINGS)/3, 2*GRID/8, couleur="#d8dee9", epaisseur=2, tag="box-input")
    
    if len(saves)>=5:
        for i in range(5):
            date = ctime(getmtime(saves[i])).split()
            fltk.rectangle(3*(GRID+SIDE+SETTINGS)/14, (6+3/2*i)*GRID/14, 11*(GRID+SIDE+SETTINGS)/14, (7+3/2*i)*GRID/14, couleur="black", epaisseur=3, tag=saves[i])
            fltk.texte((GRID+SIDE+SETTINGS)/2, (6+3/2*i)*GRID/14+30, (saves[i])[:-5]+" - "+(date[2]+"/"+str(MONTHS[date[1]])+" "+date[3]), ancrage="center", tag=saves[i])
            fltk.texte(5*(GRID+SIDE+SETTINGS)/6, (6+3/2*i)*GRID/14+10, "🗑️")
    else:
        for i in range(len(saves)):
            date = ctime(getmtime(saves[i])).split()
            fltk.rectangle(3*(GRID+SIDE+SETTINGS)/14, (6+3/2*i)*GRID/14, 11*(GRID+SIDE+SETTINGS)/14, (7+3/2*i)*GRID/14, couleur="black", epaisseur=3, tag=saves[i])
            fltk.texte((GRID+SIDE+SETTINGS)/2, (6+3/2*i)*GRID/14+30, (saves[i])[:-5]+" - "+(date[2]+"/"+str(MONTHS[date[1]])+" "+date[3]), ancrage="center", tag=saves[i])
            fltk.texte(5*(GRID+SIDE+SETTINGS)/6, (6+3/2*i)*GRID/14+10, "🗑️", tag=saves[i]+"bin")
    
    while not confirm:
        evName, event = fltk.attend_ev() #Get event
        match evName:
            case "ClicGauche":
                cible = addons.recuperer_tags(addons.objet_survole())[0]
                print(cible)
                if cible[-4:] == "save":
                    return cible

            case "Quitte":
                fltk.ferme_fenetre()
    savename = name_input((GRID+SIDE+SETTINGS)/3+20, GRID/6+30, "w")