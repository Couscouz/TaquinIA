from random import randrange
from tools import areNeightbours,getEmptyPosition
from copy import deepcopy

GOAL_GRID = [[1,2,3],[4,5,6],[7,8,None]]
PLAIN_GRID = [[1,2,3],[4,5,6],[7,8,9]]

#Melange inital de la grille, un random complet peut emmener à des resolutions impossible
def getRandomGrid(complexity=100):
    grid = GOAL_GRID
    #On part d'une grille résolue pour echanger effectuer un mouvement 
    #dans un direction aleatoire X fois (X=complexity)
    for _ in range(complexity):
        y1, x1 = getEmptyPosition(grid)
        switched = False
        while not switched:
            y2, x2 = randrange(3), randrange(3)
            if areNeightbours(y1,x1,y2,x2):
                switched = True
                newGrid = deepcopy(grid)
                newGrid[y1][x1] = grid[y2][x2]
                newGrid[y2][x2] = grid[y1][x1]
                grid = deepcopy(newGrid)
               
    return grid
