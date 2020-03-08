#!/usr/bin/env python
# coding=utf-8

import pygame, sys
from pygame.locals import *
from random import randint

WINDOWHEIGHT = 600 # hauteur de la fenetre
WINDOWWIDTH = 600 # largeur de la fenetre
TEXTCOLOR = (255, 255, 255) # blanc
BACKGROUNDCOLOR = (0, 0, 0) # noir
OBJECTSCOLOR = (255, 200, 0) # orangé
TIMBERCOLOR = (0, 155, 255)
FPS = 40 # 40 images par secondes
LARGEUR_TRONC = 50 #
LARGEUR_BRANCHE = 100
LARGEUR_TIMBER = 50
HAUTEUR_TIMBER = 60
HAUTEUR_BRANCHE = 20
MAX_TIME = 5000
TIME_BONUS = 300
ABS_TIMER = 350
ORD_TIMER = 50
HAUTEUR_TIMER = 25
LARGEUR_TIMER = 150

def terminate():
    # permet de quitter le jeu
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    # quitte le jeu au menu de depart
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # bouton fermer
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT:
                    print("left")
                elif event.key == K_RIGHT:
                    print("right")
                else:
                    return

def drawText(text, font, surface, x, y):
    # permet d'ecrire
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawTimer(timer, surface):
    # dessine le timer
    largeur = LARGEUR_TIMER * timer / 5000
    timer_rect = pygame.Rect(ABS_TIMER, ORD_TIMER, largeur, HAUTEUR_TIMER )
    pygame.draw.rect(windowSurface, TIMBERCOLOR, timer_rect)

class Timber():
    def __init__(self):
        self.direction = -1 # gauche
        self.x = 0.5 * WINDOWWIDTH - 100 # position de gauche
        self.y = WINDOWHEIGHT - HAUTEUR_TIMBER # il est pose au sol
        self.rect = pygame.Rect(self.x, self.y, LARGEUR_TIMBER, HAUTEUR_TIMBER) # le rect associe a timber
        self.score = 0
        self.time = MAX_TIME # 5 secondes
        self.alive = True # vivant


    def draw(self):
        # dessine timber
        pygame.draw.rect(windowSurface, TIMBERCOLOR, self.rect)


    def move(self, direction):
        # update la position de timber
        # qd on presse gauche, direction=-1, droite : direction=1
        self.x = 0.5 * WINDOWWIDTH + direction * 100 if direction == -1 else 0.5 * WINDOWWIDTH + direction * 100 - LARGEUR_TIMBER
        self.rect = pygame.Rect(self.x, self.y, LARGEUR_TIMBER, HAUTEUR_TIMBER) # cree le rect du timber
        arbre.move() # fait descendre les branches



    def collision(self):
        # detection d'une collision
        branche = arbre.branches[0] # on ne peut toucher que la plus basse, inutile de lire les autres
        branche_rect = pygame.Rect(branche[0], branche[1], LARGEUR_BRANCHE, HAUTEUR_BRANCHE) # peut être amélioré en updatant dynamiquement le rect des branches
        if self.rect.colliderect(branche_rect):
            # print("game over")
            self.alive = False # collision = mort
        else:
            self.score += 1 # augmente les scores
            self.time = min(self.time + TIME_BONUS, MAX_TIME) # le score est capé

    def chrono(self):
        # update le temps
        self.time -= FPS
        if self.time <= 0:
            # print("game over")
            # temps ecoulé = mort
            self.alive = False



class Arbre():
    def __init__(self):
        self.x = 0.5 * (WINDOWWIDTH - LARGEUR_TRONC)
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, LARGEUR_TRONC, WINDOWHEIGHT)
        self.branches = [[325, 0.66 * WINDOWHEIGHT], [175, 0.33 * WINDOWHEIGHT], [325, 0]]

    def draw(self):
        pygame.draw.rect(windowSurface, OBJECTSCOLOR, self.rect)
        for branche in self.branches:
            branche_rect = pygame.Rect(branche[0], branche[1], LARGEUR_BRANCHE, HAUTEUR_BRANCHE)
            pygame.draw.rect(windowSurface, OBJECTSCOLOR, branche_rect)

    def move(self):
        for i in range(len(self.branches)):
            self.branches[i][1] += 60
        if self.branches[0][1] >= WINDOWHEIGHT:
            print("AJOUT D'UNE BRANCHE !")
            del self.branches[0]
            branche = [0.5*(WINDOWWIDTH - LARGEUR_TRONC) - LARGEUR_BRANCHE if randint(0,1)==0 else 0.5*(WINDOWWIDTH + LARGEUR_TRONC), 0]
            self.branches.append(branche)
        print(self.branches)
        # Collision
        timber.collision()



# pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Timber')
# pygame.mouse.set_visible(False)

# taille et type de la fonte
font = pygame.font.SysFont(None, 48)

# show the "Start" screen
drawText('Timber', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()



while True:
    # score = 0
    # cree les objets objets
    timber = Timber()
    arbre = Arbre()



    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT:
                    timber.move(-1)
                    print("left")
                elif event.key == K_RIGHT:
                    timber.move(1)
                    print("right")
        # # recupere les touches enfoncées
        # key = pygame.key.get_pressed()
        # if key[pygame.K_LEFT]:
        #     timber.move(-1)
        #     print("left")
        # if key[pygame.K_RIGHT]:
        #     timber.move(1)
        #     print("right")



        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the scores
        drawText(str(timber.score), font, windowSurface, 0.15*WINDOWWIDTH, WINDOWHEIGHT / 10)
        # drawText(str(timber.time), font, windowSurface, 0.8*WINDOWWIDTH, WINDOWHEIGHT / 10)
        drawTimer(timber.time, windowSurface)


        # Draw the objects
        arbre.draw()
        timber.draw()
        timber.chrono()


        # pygame : tick, update
        pygame.display.update()
        if not timber.alive:
            break
        mainClock.tick(FPS)
    # pygame : update, reset
    windowSurface.fill(BACKGROUNDCOLOR)
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
