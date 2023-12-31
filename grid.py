from random import randrange
from tools import areNeightbours,getEmptyPosition
from copy import deepcopy

GOAL_GRID = [[1,2,3],[4,5,6],[7,8,None]]
PLAIN_GRID = [[1,2,3],[4,5,6],[7,8,9]]

#Melange inital de la grille, un random complet peut emmener à des resolutions impossible
#Complexité de 1000 par défaut (correspond à 1000 permutations), peut etre modifié 
def getRandomGrid(complexity=1000):
    grid = GOAL_GRID
    #On part d'une grille résolue pour echanger effectuer un mouvement 
    #dans un direction aleatoire le tout X fois (X=complexity)
    for _ in range(complexity):
        y1, x1 = getEmptyPosition(grid)
        switched = False
        while not switched:
            y2, x2 = randrange(3), randrange(3)
            if areNeightbours(y1,x1,y2,x2):
                #Si les 2 sont bien voisins on réalisé l'échange
                switched = True
                newGrid = deepcopy(grid)
                newGrid[y1][x1] = grid[y2][x2]
                newGrid[y2][x2] = grid[y1][x1]
                grid = deepcopy(newGrid)
                #possibilité d'utiliser la fonction generant les coups suivant pour l'algo A* et d'en tirer un au sort
    return grid
