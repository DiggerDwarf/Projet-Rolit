# main file

from random import randint

WIDTH, HEIGHT = 8, 8
VIDE, ROUGE, VERT, JAUNE, BLEU = 0, 1, 2, 3, 4

colors = {
    VIDE: "\033[30;40m  \033[0m",
    ROUGE: "\033[31;41m  \033[0m",
    VERT: "\033[32;42m  \033[0m",
    JAUNE: "\033[33;43m  \033[0m",
    BLEU: "\033[36;46m  \033[0m"
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