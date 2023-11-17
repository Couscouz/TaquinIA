from random import randint
from math import sqrt,pow
import copy

def getMelange():
    tirage = []
    grille = []
    for i in range(9):
        x = randint(1,9)
        while x in tirage:
            x = randint(1,9)
        tirage.append(x)
    for i in range(9):
        if tirage[i] == 9:
            tirage[i] = None
    return convertMatrix(tirage)

def convertMatrix(list):
    grille = []
    for i in range(3):
        grille.append(list[i*3:3+i*3])
    return grille

def hash(grille):
    res = ""
    for line in grille:
        for value in line:
            res += str(value)
    return res

def unhash(string):
    linear = [[],[],[]]
    for caracter in string:
        try:
            linear.append(int(caracter))
        except:
            linear.append(None)
    return convertMatrix(linear)

def afficher(grille):
    print("==========")
    for i in range(3):
        print(grille[i])


def getEmptyLocation(grille):
    for y in range(3):
        for x in range(3):
            if grille[y][x] is None:
                return y,x
    return None


def areNeightbours(y1,x1,y2,x2):
    distance = sqrt( pow(abs(y2-y1),2) + pow(abs(x2-x1),2) ) 
    return str(distance) == "1.0"

def getDistanceOfCase(value,y,x):
    temp = value
    if temp is None:
        temp = 9
        #OR return
        
    yGoal = 0
    while temp > 3:
        yGoal += 1
        temp -= 3
    xGoal = temp-1
    distance = abs(x-xGoal) + abs(y-yGoal)
    #print(f"{value} distance is {distance}")
    return distance

def getXXXWeight(grille):
    wellPlaced = 0
    for y in range(3):
        for x in range(3):
            if grille[y][x] == y*3+x:
                wellPlaced += 1
    if grille[2][2] is None:
        wellPlaced += 1
    return 9-wellPlaced

def getManhattanWeight(grille):
    total = 0
    for y in range(3):
        for x in range(3):
            total += getDistanceOfCase(grille[y][x],y,x)
    return total

def getNextGenerations(grille):
    allNextGen = [] # listes des grilles suivantes

    emptyLocationY, emptyLocationX = getEmptyLocation(grille)

    for y in range(3):
        for x in range(3):
            if areNeightbours(y,x,emptyLocationY,emptyLocationX):
                allNextGen.append(echanger(copy.deepcopy(grille),emptyLocationY,emptyLocationX,y,x))

    return allNextGen

def echanger(grille, x1, y1, x2, y2):
    if grille[y1][x1] is not None and grille[y2][x2] is not None:
        return grille
    temp = grille[y1][x1]
    resultat = grille
    resultat[y1][x1] = resultat[y2][x2]
    resultat[y2][x2] = temp
    return resultat



def processResolve(finalMove,dictParent):
    move = copy(finalMove)
    movesToProcess = [move]
    while dictParent[hash(move)] is not None:
        movesToProcess.insert(0,dictParent[hash(move)])
        move = dictParent[hash(move)]
    return movesToProcess

def process():
    initialGrille = getMelange()
    afficher(initialGrille)
    #res = echanger(grille, 2,2,1,1)
    #afficher(res)
    d = getManhattanWeight(initialGrille)

    dictWeight = {}
    dictParent = {}

    tempGrille = initialGrille
    ended = False
    coups = 0
    while not ended:
        coups += 1
        print(len(dictWeight))
        allNext = getNextGenerations(tempGrille)
        for move in allNext:
            weight = getManhattanWeight(move)
            dictWeight[hash(move)] = weight
            dictParent[hash(move)] = tempGrille

        minWeight=9
        bestMove = None
        for hashedMove,weight in dictWeight.items():
            if weight < minWeight:
                minWeight = weight
                bestMove = unhash(hashedMove)
        if minWeight == 0:      
            ended = True
            movesToProcess = processResolve(move,dictParent)
    
    print(f"Terminé en {coups} coups")
    print(movesToProcess)

    return initialGrille, movesToProcess






#allNext = getNextGenerations(grille)
#print("---------Generations-------")
#for g in allNext:
#    afficher(g)