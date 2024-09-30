# main file

from random import randint

WIDTH, HEIGHT = 8, 8
CLEAR, RED, GREEN, YELLOW, BLUE = 0, 1, 2, 3, 4

colors = {
    CLEAR: "\033[30;40m  \033[0m",
    RED: "\033[31;41m  \033[0m",
    GREEN: "\033[32;42m  \033[0m",
    YELLOW: "\033[33;43m  \033[0m",
    BLUE: "\033[36;46m  \033[0m"
}

def afficher_grille(grille):
    print("  1 2 3 4 5 6 7 8")
    for i_row in range(len(grille)):
        print(chr(ord('a') + i_row), end=" ")
        for i_elem in range(len(grille[0])):
            print(colors[grille[i_row][i_elem]], end="")
        print()

def main():
    # setup number of player and initial game state
    nb_players = 0
    while nb_players not in ("2", "3", "4"):
        nb_players = input("Combien de joueurs vont jouer ? [2-4] : ")
    nb_players = int(nb_players)
    
    grille = [[CLEAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    grille[3][3] = RED
    grille[3][4] = YELLOW
    grille[4][3] = BLUE
    grille[4][4] = GREEN
    
    afficher_grille(grille)
    

if __name__ == "__main__":
    main()