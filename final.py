from random import randint
from math import sqrt,pow
import copy
import random

def getMelange():
    grille = [[1,2,3],[4,5,6],[7,8,None]]
    for _ in range(3):
        y1 = randint(0,2)
        x1 = randint(0,2)
        switched = False
        while not switched:
            y2 = randint(0,2)
            x2 = randint(0,2)
            if areNeightbours(y1,x1,y2,x2):
                switched = True
                grille = copy.deepcopy(switch(copy.deepcopy(grille),y1,x1,y2,x2))
    return grille

def areNeightbours(y1,x1,y2,x2):
    distance = sqrt( pow(abs(y2-y1),2) + pow(abs(x2-x1),2) )
    return str(distance) == "1.0"

def switch(grille, y1, x1, y2, x2):
    resultat = copy.deepcopy(grille)
    resultat[y1][x1] = grille[y2][x2]
    resultat[y2][x2] = grille[y1][x1]
    return resultat

def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] is not None:
                value = puzzle[i][j] - 1
                goal_row, goal_col = divmod(value, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance