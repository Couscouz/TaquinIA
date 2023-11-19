import heapq
import copy
from random import randint
from math import sqrt,pow
from classes import TaquinNode

#Melange inital de la grille, un random complet peut emmener à des resolutions impossible
def getMelange(complexity):
    grille = [[1,2,3],[4,5,6],[7,8,None]]
    for _ in range(complexity):
        y1, x1 = randint(0,2), randint(0,2)
        switched = False
        while not switched:
            y2, x2 = randint(0,2), randint(0,2)
            if areNeightbours(y1,x1,y2,x2):
                switched = True
                newGrid = copy.deepcopy(grille)
                newGrid[y1][x1] = grille[y2][x2]
                newGrid[y2][x2] = grille[y1][x1]
                grille = copy.deepcopy(newGrid)
    return grille

def areNeightbours(y1,x1,y2,x2):
    distance = sqrt( pow(abs(y2-y1),2) + pow(abs(x2-x1),2) )
    return str(distance) == "1.0"

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == None:
                return i, j


def generate_neighbors(current_node):
        #On recupere les coords du carré vide
        emptyY, emptyX = get_blank_position(current_node.state)
        neighbors = []

        #On test les 4 coups (max) possibles
        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newY, newX = emptyY + move[0], emptyX + move[1]

            #On check si le coup est possible
            if 0 <= newY < 3 and 0 <= newX < 3:
                new_state = [list(row) for row in current_node.state]
                new_state[emptyY][emptyX], new_state[newY][newX] = (
                    new_state[newY][newX],
                    new_state[emptyY][emptyX],
                )
                neighbors.append(TaquinNode(new_state))

        return neighbors
    
def a_star(initial_state, goal_state):
    
    initial_node = TaquinNode(initial_state)
    goal_node = TaquinNode(goal_state)

    open_set = []  # Liste des nœuds à explorer
    closed_set = set()  # Ensemble des nœuds déjà explorés

    heapq.heappush(open_set, initial_node)

    while open_set:
        #On recupere le sommet de la pile des noeuds à explorer
        current_node = heapq.heappop(open_set)

        #Si la grille est celle à atteindre
        if current_node.state == goal_node.state:
            #On retourne le chemin de toutes les etapes parcourues
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in generate_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                neighbor.previousWeights = current_node.previousWeights + 1
                neighbor.weight = sum(
                    1 if neighbor.state[i][j] != goal_node.state[i][j] else 0
                    for i in range(3)
                    for j in range(3)
                )
                neighbor.toGetHereWeight = neighbor.previousWeights + neighbor.weight
                neighbor.parent = current_node

                heapq.heappush(open_set, neighbor)

    return None  # Aucun chemin trouvé


def process():
    
    goal_puzzle = [[1,2,3],[4,5,6],[7,8,None]]
    complexity = 100
    possible = False
    while not possible:
        # Exemple d'utilisation
        initial_puzzle = getMelange(complexity)
        
        solution_path = a_star(initial_puzzle, goal_puzzle)

        if solution_path:
            possible = True
        else:
            complexity -= 20
            
    for step, state in enumerate(solution_path):
        print(f"Step {step + 1}:")
        for row in state:
            print(row)
        print()
    print(f"compleixty={complexity}")

    return solution_path
                
process()