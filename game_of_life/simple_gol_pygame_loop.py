#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simplest implementation of GOL in pygame.

Watch the glider :)
'''

from random import randint
import pygame
import sys
from pygame.locals import *

import simplest_gol as gol

WINDOWHEIGHT = 600  # hauteur de la fenetre
WINDOWWIDTH = 600  # LARGEUR de la fenetre

BACKGROUNDCOLOR = (0, 0, 0)  # black
DOTCOLOR = (255, 255, 255)  # white
OBJCOLOR = (255, 0, 0)  # red
BESTCOLOR = (0, 255, 0)  # green
OBSTACLECOLOR = (0, 255, 255)  # cyan
TEXTCOLOR = (255, 255, 0)  # yellow

FPS = 5

LARGEUR = 30
SIZE = WINDOWWIDTH / LARGEUR

############################################################
#####################   FUNCTIONS    #######################
############################################################


def out_bound(glider):
    return max([abs(coord) for elt in glider for coord in elt]) > SIZE


def drawCell(point):
    x, y = point
    x *= -1
    y *= -1
    cell_rect = pygame.Rect(x * LARGEUR, y * LARGEUR, LARGEUR, LARGEUR)
    pygame.draw.rect(windowSurface, (255, 200, 0), cell_rect)

# ACTIONS


def terminate():
    # permet de quitter le jeu
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    # quitte le jeu au menu de depart
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

        # import pdb; pdb.set_trace()
        # Draw the scores
        # drawText(str(score), font, windowSurface, 0.5*WINDOWWIDTH, 0.5*WINDOWHEIGHT)

        gol.glider = gol.advance(gol.glider)
        if out_bound(gol.glider):
            cont = False

        # map(drawCell, gol.glider)

        for cell in gol.glider:
            drawCell(cell)

        # pygame : tick, update
        mainClock.tick(FPS)
        pygame.display.update()

    # pygame : update, reset
    pygame.display.update()
    # waitForPlayerToPressKey()
    cont = True
    gol.glider = gol.init_glider()
