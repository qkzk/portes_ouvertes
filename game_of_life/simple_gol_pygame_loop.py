#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simplest implementation of GOL in pygame.

Watch the game of life :)
'''

from random import randint
import pygame
import sys
from pygame.locals import *

import simplest_gol as gol

WINDOWHEIGHT = 700  # hauteur de la fenetre
WINDOWWIDTH = 800  # LARGEUR de la fenetre

BACKGROUNDCOLOR = (0, 0, 0)  # black
DOTCOLOR = (255, 255, 255)  # white
OBJCOLOR = (255, 0, 0)  # red
BESTCOLOR = (0, 255, 0)  # green
OBSTACLECOLOR = (0, 255, 255)  # cyan
TEXTCOLOR = (255, 200, 0)  # yellow

FPS = 20

LARGEUR = 15
SIZE = WINDOWWIDTH / LARGEUR

############################################################
#####################   FUNCTIONS    #######################
############################################################

presentation = '''

  ############################################################################
  #                                                                          #
  # Le Jeu de la vie                                                         #
  #                                                                          #
  # Le jeu de la vie est un automate cellulaire imaginé par John Conway en   #
  # 1970 et qui est le plus connu de tous les automates cellulaires.         #
  #                                                                          #
  # Le jeu de la vie est un « jeu à zéro joueur ».                           #
  #                                                                          #
  # Le jeu se déroule sur une grille infinie. Chaque case (une cellulle)     #
  # comporte deux états : vivante ou morte.                                  #
  #                                                                          #
  # À chaque tour, on calcule l'état suivant d'une cellule en fonction       #
  # de son état et de celui de ses voisines.                                 #
  #                                                                          #
  # On affiche ensuite l'état suivant.                                       #
  #                                                                          #
  # Voici les règles :                                                       #
  #                                                                          #
  # * une cellule morte possédant exactement trois voisines vivantes         #
  #     devient vivante (elle naît) ;                                        #
  # * une cellule vivante possédant deux ou trois voisines vivantes le reste,#
  #     sinon elle meurt.                                                    #
  #                                                                          #
  ############################################################################

'''


def out_bound(figure):
    return max([abs(coord) for elt in figure for coord in elt]) > SIZE


def drawCell(point):
    x, y = point
    # x *= -1
    # y *= -1
    cell_rect = pygame.Rect(x * LARGEUR, y * LARGEUR, LARGEUR, LARGEUR)
    pygame.draw.rect(windowSurface, (255, 200, 0), cell_rect)

# ACTIONS


def terminate():
    # permet de quitter le jeu
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    # quitte le jeu au menu de depart
    print(presentation)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # bouton fermer
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

# DESSIN DES ELEMENTS STATIQUES


def drawText(text, font, surface, x, y):
    # permet d'ecrire
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


############################################################
#####################   GAME INITIALISATION   ##############
############################################################


# pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Conway's game of life")
# pygame.mouse.set_visible(False)

# taille et type de la fonte
font = pygame.font.SysFont(None, 48)

# show the "Start" screen
drawText("Conway's game of life", font, windowSurface, (WINDOWWIDTH / 5), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface,
         (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

############################################################
#####################   GAME LOOP    #######################
############################################################

while True:
    score = 0
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        gol.figure = gol.advance(gol.figure)
        # if out_bound(gol.figure):
        #     cont = False

        for cell in gol.figure:
            drawCell(cell)

        # pygame : tick, update
        mainClock.tick(FPS)
        pygame.display.update()

    # pygame : update, reset
    pygame.display.update()

    cont = True
    # gol.figure = gol.init_glider()
    gol.figure = gol.init_gun()
