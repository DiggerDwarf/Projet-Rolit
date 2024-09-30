# main file

import colorama
from random import randint

WIDTH, HEIGHT = 8, 8

VIDE, ROUGE, VERT, JAUNE, BLEU = 0, 1, 2, 3, 4

colors = {
    VIDE: colorama.Back.BLACK,
    ROUGE: colorama.Back.RED,
    VERT: colorama.Back.GREEN,
    JAUNE: colorama.Back.YELLOW,
    BLEU: colorama.Back.BLUE
}


def afficher_grille(grille):
    for row in grille:
        for elem in row:
            print(colors[elem] + "  " + colorama.Back.RESET, end="")
        print()

def main():
    grille = [[randint(VIDE, BLEU) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    afficher_grille(grille)
    
    

if __name__ == "__main__":
    main()