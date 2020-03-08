#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Shortest way to implement Game of Life

Source : Jack Diederich - https://www.youtube.com/watch?v=o9pEzgHorH0

'''
import itertools
from os import system


def neighbors(point):
    x, y = point
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1


def advance(board):
    newstate = set()
    recalc = board | set(itertools.chain(*map(neighbors, board)))
    for point in recalc:
        count = sum((neigh in board) for neigh in neighbors(point))
        if count == 3 or (count == 2 and point in board):
            newstate.add(point)
    return newstate


def init_glider():
    return set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])


glider = init_glider()

if __name__ == '__main__':
    for i in range(1000):
        glider = advance(glider)
        system('clear')
        print(glider)
