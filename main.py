# main file

import colorama
from random import randint

WIDTH, HEIGHT = 8, 8

VIDE, ROUGE, VERT, JAUNE, BLEU = 0, 1, 2, 3, 4

colors = {
    VIDE: f"{colorama.Back.BLACK}  {colorama.Back.RESET}",
    ROUGE: f"{colorama.Back.RED}  {colorama.Back.RESET}",
    VERT: f"{colorama.Back.GREEN}  {colorama.Back.RESET}",
    JAUNE: f"{colorama.Back.YELLOW}  {colorama.Back.RESET}",
    BLEU: f"{colorama.Back.BLUE}  {colorama.Back.RESET}"
}


def afficher_grille(grille):
    for row in grille:
        for elem in row:
            print(colors[elem], end="")
        print()

def main():
    grille = [[randint(VIDE, BLEU) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    afficher_grille(grille)
    

if __name__ == "__main__":
    main()