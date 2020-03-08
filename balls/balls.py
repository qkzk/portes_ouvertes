#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

on va refaire ça :

https://i.imgur.com/PgfUtYN.mp4

grille carré
19 balles qui tiennent sur un rayon

rayon d'une balle = 1/20 * 1/2 * largeur = largeur / 40

segment entre chaque paire consécutive
la balle à l'exterieur tourne au rythme de 1 tour par x secondes
de l'extérieur vers l'intérieur, chaque rythme est le double du précédent

suite géométrique des vitesses angulaire

dans quoi contenir les balles ?

elles sont définies par "rayon", "angle" : 2 données
elles sont positionnées en abs, ord. Par commodité on garde aussi le numéro
    dedans
il faut aussi une vitesse
* liste de dictionnaires ? <- cleaner

C'est presque de la POO mais pas d'héritage donc on fait tout avec des fonctions

'''
import sys
import pygame
from pygame.locals import *
import numpy as np


# animation constants
WINDOWWIDTH = 600
WINDOWHEIGHT = WINDOWWIDTH
RADIUS = WINDOWWIDTH // 80
LINE_WIDTH = 3
NUM_BALLS = 19
FPS = 60  #
NUM_SECS_SLOW = 360 * 2 * 10000
SLOW_SPEED = 360 / (NUM_SECS_SLOW * FPS)  # speed of the slowest ball

# display constants
BACKGROUNDCOLOR = (34, 45, 49)  # black
DOTCOLOR = (22, 160, 133)  # white
TEXTCOLOR = DOTCOLOR  # yellow
CENTER = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)


# FUNCTIONs
def create_balls():
    '''
    Creates a ball list
    each ball is a dict with different attributes
    :param: None
    :return: (list of dict) dictionnary of balls
    '''
    balls = []
    for k in range(NUM_BALLS - 1, -1, -1):
        ball = {}
        ball["number"] = k
        ball["position"] = WINDOWWIDTH // 2 - 2 * k * RADIUS
        ball["angle"] = 0
        ball["speed"] = (k + 1) * SLOW_SPEED
        ball["abs"] = CENTER[0] + ball["position"]
        ball["ord"] = CENTER[1]
        balls.append(ball)
    return balls


def draw_balls(balls):
    '''
    draw all the balls to the pygame window
    '''
    for ball in balls:
        pygame.draw.circle(
            windowSurface,
            DOTCOLOR,
            (int(ball["abs"]), int(ball["ord"])),
            # (450, 300),
            RADIUS,
            0
        )


def draw_lines(balls):
    '''
    draw all the lines to the pygame window
    '''
    for k in range(NUM_BALLS - 1):
        ball1 = balls[k]
        ball2 = balls[k + 1]
        pygame.draw.line(
            windowSurface,
            DOTCOLOR,
            (ball1["abs"], ball1["ord"]),
            (ball2["abs"], ball2["ord"]),
            LINE_WIDTH
        )


def actuate_balls(balls):
    '''
    :SE: modifies the ball list in place
    '''
    for ball in balls:
        ball["angle"] = (ball["angle"] + ball["speed"]) % 360
        ball["abs"], ball["ord"] = rotate_center(
            ball["angle"],
            (ball["abs"], ball["ord"])
        )


def rotate(angle, vector):
    '''
    rotate a vector using numpy and matrix multiplication
    '''
    x, y = vector
    r = np.array(((np.cos(angle), -np.sin(angle)),
                  (np.sin(angle),  np.cos(angle))))
    x = np.array(vector)
    x = r.dot(x)
    return list(x)


def translate(position, vector):
    '''
    translate a vector with a simple sum
    '''
    x, y = position
    vx, vy = vector
    return x + vx, y + vy


def rotate_center(angle, vector):
    '''
    rotate a vector around the center of the screen
    first we translate the vector to bring is to (0, 0)
    then we rotate
    then we translate it back to the center
    '''
    # print(vector)
    center = [WINDOWWIDTH // 2, WINDOWHEIGHT // 2]
    opp_center = [-center[0], -center[1]]
    position = translate(vector, opp_center)
    position = rotate(angle, position)
    position = translate(position, center)
    return position


def drawText(text, font, surface, x, y):
    '''
    draws a text to the screen
    '''
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# ACTIONS


def terminate():
    '''
    kill pygame
    '''
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    '''
    action when starting the game
    '''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # bouton fermer
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# pygame initialisation
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Patterns')

# font settings
font = pygame.font.SysFont(None, 48)

# show the "Start" screen
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Patterns', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface,
         (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

############################################################
#####################   GAME LOOP    #######################
############################################################
while True:
    balls = create_balls()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        # recupere les touches enfoncées
        key = pygame.key.get_pressed()

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the animation
        draw_balls(balls)
        draw_lines(balls)

        # animate the balls
        actuate_balls(balls)

        # pygame : tick, update
        mainClock.tick(FPS)
        pygame.display.update()

    # pygame : update, reset
    pygame.display.update()
    waitForPlayerToPressKey()
