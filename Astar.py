#Sert à simuler une file
from heapq import heappop, heappush
#Sert au mélange inital
from random import randrange
#Sert à l'algo A*
from classes import TaquinNode
#Sert à copier des listes en dimensions N
import copy


def hamming_heuristic(grid):
    total = 0
    for y in range(3):
        for x in range(3):
            if grid[y][x] == y*3+x+1:
                total += 1
    return 9-total

def manhattan_heuristic(grid):
    distance = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] is not None:
                value = grid[i][j] - 1
                goal_row, goal_col = divmod(value, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

#Melange inital de la grille, un random complet peut emmener à des resolutions impossible
def getRandomGrid(complexity):
    grid = [[1,2,3],[4,5,6],[7,8,None]]
    #On part d'une grille résolue pour echanger effectuer un mouvement 
    #dans un direction aleatoire X fois (X=complexity)
    for _ in range(complexity):
        y1, x1 = randrange(3), randrange(3)
        switched = False
        while not switched:
            y2, x2 = randrange(3), randrange(3)
            if areNeightbours(y1,x1,y2,x2):
                switched = True
                newGrid = copy.deepcopy(grid)
                newGrid[y1][x1] = grid[y2][x2]
                newGrid[y2][x2] = grid[y1][x1]
                grid = copy.deepcopy(newGrid)
    return grid

#Retourne un boolean indiquant si les 2 points sont voisins (horizontalement ou verticalement)
#Etre voisin en diagonale n'est pas correct car pas de mouvement en diagonale
def areNeightbours(y1,x1,y2,x2):
    #Decalage horizontal et vertical de 1 strictement (car 0 signifie case identique, et > 1 diagonale ou + loin)
    return abs(y2-y1) + abs(x2-x1) == 1

#Retourne l'emplacement du carré vide
def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == None:
                return i, j

#Retourne l'ensemble des voisins du carré vide
def generate_neighbors(current_node):
        #On recupere les coords du carré vide
        emptyY, emptyX = get_blank_position(current_node.grid)
        neighbors = []

        #On test les 4 coups (max) possibles
        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newY, newX = emptyY + move[0], emptyX + move[1]

            #On check si le coup est possible (dans la grille)
            if 0 <= newY < 3 and 0 <= newX < 3:
                new_state = copy.deepcopy(current_node.grid)
                #on genere le coup suivant et on l'ajoute à la liste résultat
                new_state[emptyY][emptyX] = current_node.grid[newY][newX]
                new_state[newY][newX] = current_node.grid[emptyY][emptyX]
                neighbors.append(TaquinNode(new_state))

        return neighbors
    
#Algo principal qui retourne un chemin (liste de grilles) pour arriver à 'goalGrid' depuis 'initialGrid'
def a_star(initialGrid, goalGrid, heuristic_fct):
    
    initial_node = TaquinNode(initialGrid)
    goal_node = TaquinNode(goalGrid)

    # Liste des nœuds à explorer
    open_set = []  
    # Ensemble des nœuds déjà explorés
    closed_set = set()  

    heappush(open_set, initial_node)

    while open_set:
        #On recupere le sommet de la pile des noeuds à explorer
        current_node = heappop(open_set)

        #Si la grille est celle à atteindre
        if current_node.grid == goal_node.grid:
            #On retourne le chemin de toutes les etapes parcourues
            path = []
            while current_node:
                path.append(current_node.grid)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(map(tuple, current_node.grid)))

        for neighbor in generate_neighbors(current_node):
            if tuple(map(tuple, neighbor.grid)) not in closed_set:
                neighbor.previousWeights = current_node.previousWeights + 1
                neighbor.weight = heuristic_fct(neighbor.grid)
                neighbor.toGetHereWeight = neighbor.previousWeights + neighbor.weight
                neighbor.parent = current_node

                heappush(open_set, neighbor)

    return None  # Aucun chemin trouvé


def process():
    
    goalGrid = [[1,2,3],[4,5,6],[7,8,None]]
    complexity = 100
    possible = False
    heuristic_Fct = manhattan_heuristic
    # heuristic_Fct = hamming_heuristic
    
    while not possible:
        # Exemple d'utilisation
        initialGrid = getRandomGrid(complexity)
        
        solution_path = a_star(initialGrid, goalGrid, heuristic_Fct)

        if solution_path:
            possible = True
        else:
            complexity -= 10
            
    for step, state in enumerate(solution_path):
        print(f"Step {step + 1}:")
        for row in state:
            print(row)
        print()
    print(f"compleixty={complexity}")

    return solution_path

process()