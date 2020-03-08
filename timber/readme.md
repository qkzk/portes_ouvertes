'''
title: 'MineSweeper with Pygame Zero'
author: 'qkzk'
date: '2019/12/16'
'''

# Mine Sweeper

bizarrement je n'ai jamais vraiment pensé à ce jeu.
Donc c'est parti, pourquoi pas...

# Pygame Zero

[pygame zero](https://pygame-zero.readthedocs.io/en/stable/index.html)

# Principe

l'idée est de refaire le [minesweeper de google](https://www.google.com/search?q=minesweeper)


# Change log

2019/12/16 : tilemap avec les bombes et les voisins
2019/12/17 : le jeu est jouable

# Done

* cliquer sur une tile
* révéler les autres cf recursion contagion
  * définir 7 images : 1, 2, ..., 7 bombes
  * révéler les nombres de bombes des bordures (voisin revele + pas bombe soi meme)
* mourir
* gagner
* graphismes
* ui : afficher nombre de bombes restantes

# TODO

* bug : toujours un pb d'exploration ???
* remplacer les textes par des images, améliorer lisibilité
* animation de mort
* menu pour changer la difficulté
* visuel qui explique le début de partie
