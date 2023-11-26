from heapq import heappop, heappush #Sert à simuler une file
from classes import TaquinNode #Classe d'un noeud, essentiel pour A*
from tools import getEmptyPosition #Fonctions annexes agissant sur une grille
from heuristic import hamming_heuristic,manhattan_heuristic #2 fcts de calcul d'heuristic pour une grille donnée
from grid import GOAL_GRID, getRandomGrid 
from copy import deepcopy #Sert à copier des listes en dimensions N

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
    
    #Noeud du mélange initial
    initial_node = TaquinNode(initialGrid)
    #Noeud d'une grille finale
    goal_node = TaquinNode(goalGrid)

    # Liste des nœuds à explorer
    toExplore = []  
    # Ensemble des nœuds déjà explorés
    explored_set = set()  

    #Ajout du noeud racine dans la file des noeuds à explorer
    heappush(toExplore, initial_node)

    while toExplore:
        #On recupere le sommet de la pile des noeuds à explorer
        current_node = heappop(toExplore)

        #Si la grille est celle à atteindre
        if current_node.grid == goal_node.grid:
            #On retourne le chemin de toutes les etapes parcourues
            path = []
            while current_node:
                #Pour chaque noeud parcourue on l'ajoute à la liste résultat
                #Ainsi on remonte jusqu'a notre grille initiale (mélangée)
                path.append(current_node.grid)
                current_node = current_node.parent
            #Retourne la liste des chemins inversées
            return path[::-1]

        #On marque le noeud comme exploré
        explored_set.add(tuple(map(tuple, current_node.grid)))

        #Pour chaque suivant on l'ajoute au graphe (si il n'est pas deja dedans), en definissant son poids
        #Amelioration possible : si il est deja dans le graphe et 
        #que le poids pour y parvenir est inferieur à l'actuel on le met à jour
        for neighbor in generateNeighbors(current_node):
            if tuple(map(tuple, neighbor.grid)) not in explored_set:
                #Si le noeud n'a pas été exploré on le calcule (poids actuel, poids pour y parvenir...)
                neighbor.previousWeights = current_node.previousWeights + 1
                neighbor.weight = heuristic_fct(neighbor.grid) #calcul du poids du noeud
                neighbor.toGetHereWeight = neighbor.previousWeights + neighbor.weight
                neighbor.parent = current_node #Definition du noeud parent

                #Ajout du noeud dans la file de ceux à explorer
                heappush(toExplore, neighbor)

    return None  # Aucun chemin trouvé, n'arrive que si le mélange initial est incorrect

#Permet d'autiliser l'algo A*
def process(heuristic_Fct = manhattan_heuristic):
    
    # heuristic_Fct = manhattan_heuristic
    # heuristic_Fct = hamming_heuristic

    #Calcul d'une grille initiale aléatoire
    initialGrid = getRandomGrid()
    #On retourne la liste des étapes (grilles) de la solution calculée
    return a_star(initialGrid, GOAL_GRID, heuristic_Fct)
