from colors import BLUE,BLACK,WHITE,YELLOW
from grid import GOAL_GRID,PLAIN_GRID
from tools import getEmptyPosition,areNeightbours,dim3to1
from Astar import process as AstarGeneration
from includes.images import allPart
import includes.window as window
import includes.startButton as startButton
import pygame


pygame.init()

fontTitle = pygame.font.Font('freesansbold.ttf', 72)
fontIndics = pygame.font.Font('freesansbold.ttf', 48)

titre = pygame.display.set_caption("Taquin")
fenetre = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
clock = pygame.time.Clock()

whiteSquare = pygame.Surface((150,150))
whiteSquare.fill(WHITE)

#---------------------------------------------  

#Initialisation de la partie en determinant la grille de depart et sa resolution (res path[0] et path)
def initGame():
    path = AstarGeneration()
    return path,path[0],path[0],0

#Cloture de la partie, mise en place du message de fin correspondant au resultat
def endGame(played,sentence):
    endMessage = fontIndics.render(sentence, True, BLACK)
    msgRect = endMessage.get_rect()
    msgRect.center = (window.WIDTH // 2, window.HEIGHT // 8) 
    return endMessage,msgRect,played+1

#Check les grilles pour determiner la suite de la partie (gagnant, égalité, partie non terminée)
def checkWin(leftGrid,rightGrid):
    if leftGrid == GOAL_GRID and rightGrid != GOAL_GRID:
        return "Bien joué vous avez gagné!"
    elif leftGrid != GOAL_GRID and rightGrid == GOAL_GRID:
        return "Dommage vous avez perdu..."
    elif leftGrid == GOAL_GRID and rightGrid == GOAL_GRID:
        return "Egalité !"
    else:
        return None

#Effectue un mouvement sur une grille depuis la case cliquée
def processMove(grid, click):
    noneY, noneX = getEmptyPosition(grid)
    if not areNeightbours(noneX,noneY,click[1],click[0]):
        return False
    for y in range(3):
        for x in range(3):
            if grid[y][x] == None:
                grid[y][x] = grid[click[0]][click[1]]
    grid[click[0]][click[1]] = None
    return True

#Superpose les cases d'une grille sur la fenetre 
def refreshGrid(background, grid):
    index = 0
    order = dim3to1(grid)
    for y in [0, 150, 300]:
        for x in [0, 150, 300]:
            if order[index] != None:
                background.blit(allPart[order[index]-1], (x,y))
            else:
                background.blit(whiteSquare, (x,y))
            index += 1

#Affichage des zones de la fenetre et de la ligne centrale
def graphics(fenetre,background,leftSquare,rightSquare):
    fenetre.blit(background, (0, 0))
    fenetre.blit(leftSquare, (95, 175))
    fenetre.blit(rightSquare, (735, 175))
    pygame.draw.line(fenetre, BLACK, (640,150), (640,650))


#Return Y,X, isLeft
def getSquareFromClick(location):
    horizontal = [(95,245), (246, 395), (396,545)]
    vertical = [(175,325),(326,475),(476,625)]
    offset = 0
    
    if location[0] > 640:
        offset = 640    
    for y in range(3):
        for x in range(3):
            if ((offset+horizontal[x][0]) < location[0] <= (offset+horizontal[x][1])) and (vertical[y][0] < location[1] <= vertical[y][1]):
                return y,x, (offset==0)

    return None

def main():
    
    leftGrid = PLAIN_GRID
    rightGrid = PLAIN_GRID
    
    running = True
    status = "waiting" #playing
    
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())
    background.fill(BLUE)
    
    #Carré blanc du fond de taquin
    leftSquare = pygame.Surface((450,450))
    leftSquare.fill(WHITE)
    rightSquare = pygame.Surface((450,450))
    leftSquare.fill(WHITE)

    #Compteur de coups
    moveCounter = fontIndics.render(f"Coups joués : 0", True, BLACK)
    moveRect = moveCounter.get_rect()
    moveRect.center = (window.WIDTH // 2, window.HEIGHT // 8)
    
    
    
    coups = 0  # nb de coups joués dans la partie actuelle
    played = 0 # nb de parties jouées
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if status == "playing":
                    analyse = getSquareFromClick(pos)
                    if analyse:
                        if processMove(leftGrid, analyse):
                            coups += 1
                            moveCounter = fontIndics.render(f"Coups joués : {coups}", True, BLACK)
                            rightGrid = path[coups]
                        sentence = checkWin(leftGrid,rightGrid)
                        if sentence is not None:
                            status = "waiting"
                            endMessage,msgRect,played = endGame(played,sentence)     
                        
                elif status == "waiting":
                    if startButton.isClicked(pos):
                        status = "playing"
                        path,leftGrid,rightGrid,coups = initGame()
                        moveCounter = fontIndics.render(f"Coups joués : 0", True, BLACK)
        #----------Drawnings-------
        
        graphics(fenetre, background, leftSquare, rightSquare)
        
        
        
        if status == "waiting":
            fenetre.blit(startButton.content, startButton.rect)
            if played > 0:
                fenetre.blit(endMessage, msgRect)
        elif status == "playing":
            fenetre.blit(moveCounter, moveRect)

        #leftSquare.blit(img, (0,0))
        refreshGrid(leftSquare,leftGrid)
        refreshGrid(rightSquare,rightGrid)
        
        # Rafraîchissement de l'écran toutes les 10ms
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

if __name__ == '__main__':
    main()