to render the markdown document:
 - paste its contents [here](https://md-to-pdf.fly.dev/)
 - remove this header
 - select the ``pdflatex`` render mode (consistency, i use it)
 - press convert and download

# Projet Rolit

## Le contexte

Ci-dessous, ``"le client"`` réfère au chargé de TP.

Le besoin exprimé par le client est de concevoir une version informatique du jeu ``"Rolit"``.

## L'équipe

Ci-dessous, ``"l'équipe"`` réfère à Nathan KUNTZ, Jeremy LI et Lilian VISTE.

Tous les membres de l'équipe appartiennent à l'organisation ``"Groupe de projet 12-6"``, filiale de l'entité ``"Université Gustave Eiffel"``.

Notre équipe se répartit uniformément les rôles de manière à ce que le projet avance avec l'accord de chaque membre pour chaque fonctionnalité ou améliorations ajoutée. Cela nous permet d'être synchrones quant aux modifications que le jeu subit au fil du temps et donc d'être plus efficaces.\

## Le budget

L'équipe se propose de ne pas être rémunérée pour son travail passionné en échange d'une bonne note sur "Linkedin". *hum hum*

En raison de cette absence de budget, l'équipe n'aura pas recours à la sous-traitance.


## Le planning

### Premier point d'étape

Date du rendez-vous : ``21 novembre 2024, 16:45``

Ordre du rendez-vous : discuter du premier prototype et des besoins supplémentaires du client

Livrable présenté : premier prototype, version console jouable du jeu ``Rolit``

## Le livrable

### Première itération

La première itération consiste en une version jouable à la console du jeu.

Au lancement du programme, le joueur se voit demander combien de joueurs vont jouer, de ``2`` à ``4``.\
Le programme indique ensuite les couleurs qui vont être données aux pions et laisse le temps aux joueurs de décider l'attribution des couleurs entre eux.

Le plateau de jeu est affiché avec des couleurs, mais également avec des lettres représentant celles-ci, pour rendre la compréhension du jeu plus facile au personnes avec une déficience dans la perception des couleurs.

Lors de l'affichage du plateau, à chaque colonne est associée un chiffre de ``1`` à ``8`` et à chaque ligne est associée une lettre de ``a`` à ``h``.\
En se servant de ces identifiants, le joueur pourra indiquer dans quelle case il veut placer sa boule (ex: ``d3`` placera la boule dans la ligne ``3`` et la colonne ``d``)

La capture des boules est faite automatiquement.

Quand tout le plateau est rempli, le programme indique le score de chaque joueur, c'est-à-dire le nombre de boules de leur couleur sur le plateau.

## Pistes d'améliorations

* Implémenter une version par interface graphique (se référer aux maquettes)
* Effets sonores
* Adversaire virtuel
* Couleurs variées selon les pions, plus "naturelles"

## Les technologies

Sous la demande du client, Le programme sera écrit dans le langage de programmation python.\
Sous la demande du client, l'interface graphiques sera réalisée en ayant recours à la librairie fltk.\
Sous la demande du client, le code sera rédigé de façon à être compréhensible et réutilisable.

Le code sera placé sous une license MIT standard:

``Copyright (c) 2024 Nathan KUNTZ, Jeremy LI and Lilian VISTE``