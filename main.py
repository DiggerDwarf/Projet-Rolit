# main file
import argparse, modules.graphical as graphical, modules.cmd as cmd

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

    if args.nb_players < 2 and args.nb_players != 0:
        print("Cannot have this little players, redirecting to choose prompt")
        args.nb_players = 0
    elif args.nb_players > 4:
        print("Cannot have more than 4 players, truncating to 4.")
        args.nb_players = 4

    # enter correct game loop based on dislpay mode
    if args.graphical:
        graphical.mainloop_window (args.nb_players, args.nb_manches, args.ai)
    else:
        cmd.mainloop_cmdline(args.nb_players, args.nb_manches, args.ai)
