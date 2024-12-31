# UGE: Rolit
Jeu de plateau Rolit en Python

## Installation

1. Installer Python 3.10 ou plus récent
2. Télécharger le code source
3. Décompresser le fichier téléchargé

## Utilisation

1. Ouvrir un terminal dans le dossier où se trouve le code source
2. Exécuter la commande `python3 main.py`

### Arguments optionnels

- `--graphical`/`--no-graphical`: Utiliser le mode graphique ou non (activé par défaut) (**ATTENTION**: le mode console n'est plus supporté, certaines fonctionnalités ne sont donc disponibles que dans le mode graphique)
- `--nb_players <nombre de joueurs>` ou `-n <nombre de joueurs>`: Nombre de joueurs (1 à 4)
- `--nb_manches <nombre de manches>` ou `-m <nombre de manches>`: Nombre de manches
- `--ai`: Activer les IA, en mode graphique, le nombre d'IA sera choisit par l'utilisateur, en mode console, le nombre d'IA sera égal au nombre de joueurs - 1 (i.e. si l'argument `--nb_players` est égal à 4, il y aura 3 IA et 1 joueur humain)

## Bug connus

- Avec une ancienne version de `tkinter`, il est possible que le jeu plante ou crash. (Seg fault en Python ???)
- Le jeu peut ne pas fonctionner correctement sur Linux, notamment pour l'affichage des emojis (le bouton paramètre, le bouton retour dans les paramètres, les couronnes, etc.)
