"""Cmd game"""

from modules.rollit import *
import os

# define colors as letters and ANSI escape codes
SELECTED_COLORS = {
    CLEAR: "\033[40m • \033[0m",
    RED: "\033[30;41m R \033[0m",
    GREEN: "\033[30;42m V \033[0m",
    YELLOW: "\033[30;43m J \033[0m",
    BLUE: "\033[30;46m B \033[0m"
}

def clear() -> None:
    """Clear the console"""
    # just checking the os version to send correct clear command
    os.system("cls" if os.name == "nt" else "clear")


def display_grid_cmdline(grid: list[list[int]]) -> None:
    """Display the game grid onto the terminal

    :param grid: game grid"""
    # print column indices
    print("   1  2  3  4  5  6  7  8")
    for i_row in range(len(grid)):
        # print row indices
        print(chr(ord('a') + i_row), end=" ")
        # print ball colors according to lookup table `colors`
        for i_elem in range(len(grid[0])):
            print(SELECTED_COLORS[grid[i_row][i_elem]], end="")
        # print new line
        print()


def mainloop(nb_players: int, nb_rounds: int, ai: bool) -> None:
    """Main game loop

    :param nb_players: number of players
    :param nb_rounds: number of rounds
    :param ai: if the player wants to play against the AI"""
    # setup number of player and initial game state
    clear()
    if nb_players == 0:
        while nb_players not in ("2", "3", "4"):
            nb_players = input("Combien de joueurs vont jouer ? [2-4] : ")
        nb_players = int(nb_players)

    if nb_rounds == 0:
        nb_rounds = input("Combien de manches voulez-vous jouer ? (par défaut 1): ")
        if nb_rounds.isnumeric():
            nb_rounds = int(nb_rounds)
        else:
            nb_rounds = 1

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

    for i in range(nb_rounds):
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
                    playerInput = input(f"Joueur {COLOR_NAMES[player]}, Emplacement de votre prochaine boule (ex: a1, A1) : ").lower()
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
            print(f"Le gagnant de la manche est le joueur {COLOR_NAMES[winner[0]]} avec {max_score} points !")
        else:
            print(f"Egalité entre les joueurs", end=" ")
            for p in winner:
                print(COLOR_NAMES[p], end=" ")
            print(f"avec un score de {max_score} pour la manche")
        rounds_won[winner[0]] += 1

    #get the max score and the player who won the game
    max_score = max(score_tot.values())
    winner = [k for k, v in score_tot.items() if v == max_score]
    if len(winner) == 1:
        print(f"Le gagnant de la partie est le joueur {COLOR_NAMES[winner[0]]} avec {max_score} points !")
    else:
        print(f"Egalité entre les joueurs", end=" ")
        for p in winner:
            print(COLOR_NAMES[p], end=" ")
        print(f"avec un score de {max_score} pour la partie")