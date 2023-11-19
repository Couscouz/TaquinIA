from random import randint
from math import sqrt,pow
import copy

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

def convertMatrix(list):
    grille = []
    for i in range(3):
        grille.append(list[i*3:3+i*3])
    return grille

def hash(grille):
    res = ""
    for line in grille:
        for value in line:
            if value is None:
                res += 'N'
            else:
                res += str(value)
    return res

def unhash(string):
    linear = []
    for caracter in string:
        try:
            linear.append(int(caracter))
        except:
            linear.append(None)
    return convertMatrix(linear)

def afficher(grille):
    #print(f"==== w={getXXXWeight(grille)} =====")
    for i in range(3):
        print(grille[i])


def getEmptyLocation(grille):
    for y in range(3):
        for x in range(3):
            if grille[y][x] is None:
                return y,x
    print("laa")
    afficher(grille)
    return None, None


def areNeightbours(y1,x1,y2,x2):
    distance = sqrt( pow(abs(y2-y1),2) + pow(abs(x2-x1),2) )
    return str(distance) == "1.0"

def getXXXWeight(grille):
    wellPlaced = 0
    for y in range(3):
        for x in range(3):
            if grille[y][x] == y*3+x+1:
                wellPlaced += 1
    if grille[2][2] is None:
        wellPlaced += 1
    return 9-wellPlaced

def getManhattanWeight(grille):
    total = 0
    for y in range(3):
        for x in range(3):
            if grille[y][x] is not None:
                value = grille[y][x] - 1
                goalY, goalX = divmod(value, 3)
                total += abs(y - goalY) + abs(x - goalX)
    return total

def getNextGenerations(grille):
    allNextGen = [] # listes des grilles suivantes

    emptyLocationY, emptyLocationX = getEmptyLocation(grille)
    for y in range(3):
        for x in range(3):
            if areNeightbours(y,x,emptyLocationY,emptyLocationX):
                allNextGen.append(switch(copy.deepcopy(grille),emptyLocationY,emptyLocationX,y,x))

    return allNextGen

def switch(grille, y1, x1, y2, x2):
    resultat = copy.deepcopy(grille)
    resultat[y1][x1] = grille[y2][x2]
    resultat[y2][x2] = grille[y1][x1]
    return resultat

def processResolve(finalMove,dictParent):
    move = copy.deepcopy(finalMove)
    movesToProcess = [move]
    while dictParent[hash(move)] is not None:
        movesToProcess.insert(0,dictParent[hash(move)])
        move = dictParent[hash(move)]
    return movesToProcess

def getBestMove(allWeights,done):
    minWeight = 50
    move = None
    for grille,weight in allWeights.items():
        if weight < minWeight and not grille in done:
            minWeight = weight
            move = unhash(grille)
    
    return move,minWeight

def afficherAll(all):
    print("------debut-ALL------")
    for move in all:
        afficher(move)
    print("-------fin-ALL-------")

def process():
    initialGrille = getMelange()
    afficher(initialGrille)
    #res = echanger(grille, 2,2,1,1)
    #afficher(res)

    dictWeight = {}
    dictParent = {}
    
    done = []
    
    minWeight = 500

    tempGrille = initialGrille
    ended = False
    coups = 0
    while not ended:
        coups += 1
        if tempGrille == [[1,2,3],[4,5,6],[7,8,None]]:
            print("fini")
            break
        allNext = getNextGenerations(tempGrille)
        afficherAll(allNext)
        for move in allNext:
            weight = getManhattanWeight(move)
            dictWeight[hash(move)] = weight
            dictParent[hash(move)] = tempGrille

        print(dictWeight)
        #print(dictParent)
        bestMove,minWeight = getBestMove(dictWeight, done)
        
        dictWeight.pop(hash(bestMove))
        done.append(hash(bestMove))

        if minWeight == 0:      
            ended = True
            movesToProcess = processResolve(move,dictParent)
            print(movesToProcess)
        else:
            tempGrille = copy.deepcopy(bestMove)

        if coups == 200 :
            ended = True
        print("move to proces is :")
        afficher(bestMove)
        print(f"coups={coups} minWeight={minWeight}")
        print(f"len dictWeight={len(dictWeight)}")
        print(f"len dictParent={len(dictParent)}")
        
    print(f"Terminé en {coups} coups")
    #print(movesToProcess)

    #return initialGrille, movesToProcess

def test():
    
    grille = [[2,7,3],[4,5,6],[1,8,None]]
    temp = hash(grille)
    print(getXXXWeight(grille))

process()



