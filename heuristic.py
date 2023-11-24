#Renvoie le poids d'une grille suivant le calcul d'Hamming
#Une case mal placée equivaut à 1 point, retourne le total des points de la grille
def hamming_heuristic(grid):
    total = 0
    for y in range(3):
        for x in range(3):
            if grid[y][x] == y*3+x+1:
                total += 1
    return 9-total

#Renvoie le poids d'une grille suivant le calcul de Manhattan
#Addition des distances entre les valeurs et l'endroit où elles devraient l'etre
#1 deplacement vertical/horizontal = 1 point
def manhattan_heuristic(grid):
    distance = 0
    for y in range(3):
        for x in range(3):
            #On ecarte None car non pertinent à traiter
            if grid[y][x] is not None:
                value = grid[y][x] - 1 #Car 1 situé en (0,0)
                goalY, goalX = divmod(value, 3) #Renvoi les coordonnées de l'emplacement final de la valeur
                distance += abs(y - goalY) + abs(x - goalX) #Recupere la distance avec l'emplacement actuel
    return distance