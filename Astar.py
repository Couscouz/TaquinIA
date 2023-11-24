#Sert à simuler une file
from heapq import heappop, heappush
#Sert à l'algo A*
from classes import TaquinNode
#Fonctions annexes agissant sur une grille
from tools import getEmptyPosition
#Calculs d'heuristic pour une grille donnée
from heuristic import hamming_heuristic,manhattan_heuristic
#Grille de départ et generation de grille aleatoire
from grid import GOAL_GRID, getRandomGrid
#Sert à copier des listes en dimensions N
from copy import deepcopy


#Retourne l'ensemble des voisins du carré vide
def generateNeighbors(current_node):
        #On recupere les coords du carré vide
        emptyY, emptyX = getEmptyPosition(current_node.grid)
        neighbors = []

        #On test les 4 coups (max) possibles
        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newY, newX = emptyY + move[0], emptyX + move[1]

            #On check si le coup est possible (dans la grille)
            if 0 <= newY < 3 and 0 <= newX < 3:
                new_state = deepcopy(current_node.grid)
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

        for neighbor in generateNeighbors(current_node):
            if tuple(map(tuple, neighbor.grid)) not in closed_set:
                neighbor.previousWeights = current_node.previousWeights + 1
                neighbor.weight = heuristic_fct(neighbor.grid)
                neighbor.toGetHereWeight = neighbor.previousWeights + neighbor.weight
                neighbor.parent = current_node

                heappush(open_set, neighbor)

    return None  # Aucun chemin trouvé


def process(complexity=100):
    
    
    possible = False
    heuristic_Fct = manhattan_heuristic
    # heuristic_Fct = hamming_heuristic
    
    while not possible:
        # Exemple d'utilisation
        initialGrid = getRandomGrid(complexity)
        
        solution_path = a_star(initialGrid, GOAL_GRID, heuristic_Fct)

        if solution_path:
            possible = True
        
        print(f"not possible, complex={complexity}")
    # for step, state in enumerate(solution_path):
    #     print(f"Step {step + 1}:")
    #     for row in state:
    #         print(row)
    #     print()
    print(f"compleixty={complexity}")

    return solution_path
