#Retourne l'emplacement du carré vide
def getEmptyPosition(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == None:
                return i, j
            
#Retourne un boolean indiquant si les 2 points sont voisins (horizontalement ou verticalement)
#Etre voisin en diagonale n'est pas correct car pas de mouvement en diagonale
def areNeightbours(y1,x1,y2,x2):
    #Decalage horizontal et vertical de 1 strictement (car 0 signifie case identique, et > 1 diagonale ou + loin)
    return abs(y2-y1) + abs(x2-x1) == 1

#Convertit une matrice 3x3 en 1x9
def dim3to1(grid):
    res = []
    for y in range(3):
        for x in range(3):
            res.append(grid[y][x])
    return res