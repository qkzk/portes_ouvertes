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


def init_gun():
    return set([
        (1, 5), (1, 6), (2, 5), (2, 6),
        (11, 5), (11, 6), (11, 7),
        (12, 4),
        (12, 8),
        (13, 3), (14, 3),
        (13, 9), (14, 9),
        (15, 6),
        (16, 4),
        (16, 8),
        (17, 5), (17, 6), (17, 7),
        (18, 6),
        (21, 3), (22, 3), (21, 4), (22, 4), (21, 5), (22, 5),
        (23, 2),
        (23, 6),
        (25, 1), (25, 2),
        (25, 6), (25, 7),
        (35, 3), (36, 3), (35, 4), (36, 4)
    ])


figure = init_gun()
# figure = init_glider()

if __name__ == '__main__':
    for i in range(1000):
        figure = advance(figure)
        system('clear')
        print(figure)
