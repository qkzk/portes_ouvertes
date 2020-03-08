#!/usr/bin/env python
# coding=utf-8
'''
solve a sudoku
'''
'''
1 à 9 en ligne
1 à 9 en colonne
1 à 9 ds chaque sous carré 3x3

0 si on ne connait pas la valeur
'''
'''
La méthode la plus rapide pour un ordinateur consiste à essayer systématiquement, l’un après l’autre, tous les candidats restants. Appliquée récursivement, elle peut résoudre tous les puzzles
'''

'''
A brute force algorithm visits the empty cells in some order, filling in digits sequentially, or backtracking when the number is found to be not valid.
Briefly, a program would solve a puzzle by placing the digit "1" in the first cell and checking if it is allowed to be there.
If there are no violations (checking row, column, and box constraints) then the algorithm advances to the next cell, and places a "1" in that cell.
When checking for violations, if it is discovered that the "1" is not allowed, the value is advanced to "2".
If a cell is discovered where none of the 9 digits is allowed, then the algorithm leaves that cell blank and moves back to the previous cell.
The value in that cell is then incremented by one.
This is repeated until the allowed value in the last (81st) cell is discovered.
'''

'''
backtracking avec recursion minimale
'''




import numpy as np
import time
def isValid(grille, n, valeur):
    '''
    renvoie True si on peut mettre "valeur" en position "n"
    '''
    # coordonnées des elements
    # exemple n = 37
    i = n // 9                  # ligne : 4
    j = n % 9                  # colonne :  1
    k = n // 27 * 3             # ligne de debut de bloc : 3
    l = (n % 9) // 3 * 3        # colonne de debut de bloc : 0

    # reunion des elements deja presents ds ligne, col, bloc
    valeurs_presentes = (
        set(grille[i].A1) |
        set(grille.T[j].A1) |
        set(grille[k:k+3, l:l+3].A1)
    )
    if valeur in valeurs_presentes:
        # la valeur proposee est deja presente, la grille est fausse
        return False
    else:
        # la valeur proposee n'apparait pas encore, la grille est tjrs valide
        return True


def sudoku(grille, n=0):

    # prochain element et test de victoire
    while grille.A1[n] != 0:
        n += 1
        if n >= 81:
            return True
    # coordonnées des elements
    # exemple n = 37
    i = n // 9                  # ligne : 4
    j = n % 9                  # colonne :  1
    k = n // 27 * 3             # ligne de debut de bloc : 3
    l = (n % 9) // 3 * 3        # colonne de debut de bloc : 0

    # candidats possibles pour la cellule en cours
    # {0,...,9} - valeurs des lignes, colonnes, bloc
    valeurs_possibles = set(range(1, 10)) - (
        set(grille[i].A1) |
        set(grille.T[j].A1) |
        set(grille[k:k+3, l:l+3].A1)
    )
    # # affichages intermédiaires
    # print("\n" * 10)
    # print(grille)
    # print("i: {} - j: {} - valeurs possibles {}".format(i, j, valeurs_possibles))
    # time.sleep(10)
    # # fin des affichages intermédiaires
    for valeur in valeurs_possibles:
        if isValid(grille, n, valeur):  # la grille est possible
            grille[i, j] = valeur
            # # affichages intermédiaires
            print(n)
            print("ligne {0} colonne {1} - valeur {2}\n".format(i, j, valeur))

            print(grille)
            # time.sleep(3)
            # # fin des affichages intermédiaires
            if sudoku(grille, n):
                return True
    else:
        # on n'arrive ici que si aucune valeur de i j ne peut correspondre
        grille[i, j] = 0
        return False


if __name__ == '__main__':
    entree = np.matrix("""
        8 0 0 1 0 9 0 7 0;
        0 9 0 0 0 0 8 0 0;
        5 0 3 0 4 0 0 0 0;
        0 0 0 0 0 0 7 9 0;
        0 0 7 2 6 5 3 0 0;
        0 3 8 0 0 0 0 0 0;
        0 0 0 0 9 0 4 0 1;
        0 0 6 0 0 0 0 2 0;
        0 5 0 4 0 2 0 0 3
    """)

    entree1 = np.matrix(
        [[5, 1, 7, 6, 0, 0, 0, 3, 4],
         [2, 8, 9, 0, 0, 4, 0, 0, 0],
         [3, 4, 6, 2, 0, 5, 0, 9, 0],
         [6, 0, 2, 0, 0, 0, 0, 1, 0],
         [0, 3, 8, 0, 0, 6, 0, 4, 7],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 9, 0, 0, 0, 0, 0, 7, 8],
         [7, 0, 3, 4, 0, 0, 5, 6, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    )

    # print(isValid(entree1, 1, 8))
    print(entree)
    start = time.time()
    sudoku(entree)
    end = time.time()
    print(entree)
    print("{} seconds".format(end - start))
    #
    #
    #
    #
    #
    ##
    ##
    ##
    ##
    ##
    ##
    #
