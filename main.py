from colors import BLUE,BLACK,WHITE,YELLOW

from tools import getEmptyPosition,areNeightbours,dim3to1
from Astar import process as AstarGeneration
import pygame

pygame.init()
titre = pygame.display.set_caption("Taquin")

clock = pygame.time.Clock()

windowHeight = 800
windowWidth = 1280

btnWidth = 450
btnHeight = 100

font = pygame.font.Font('freesansbold.ttf', 72)

img = pygame.image.load("img/PDPPaular.png")
img = pygame.transform.scale(img, (450,450))

whiteSquare = pygame.Surface((150,150))
whiteSquare.fill(WHITE)

finalGrid = [[1,2,3],[4,5,6],[7,8,None]]

allPart = []
for i in range(9):
    temp = pygame.image.load(f"img/{i+1}.jpg")
    allPart.append(pygame.transform.scale(temp, (150,150)))

#---------------------------------------------

def checkWin(grid,status):
    if grid == finalGrid:
        status = "finished"
        print("Bien joué !")
    
def processMove(grid, click):
    noneY, noneX = getEmptyPosition(grid)
    if not areNeightbours(noneX,noneY,click[1],click[0]):
        return
    for y in range(3):
        for x in range(3):
            if grid[y][x] == None:
                grid[y][x] = grid[click[0]][click[1]]
    grid[click[0]][click[1]] = None

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

def backgrounds(fenetre,background,leftSquare,rightSquare):
    fenetre.blit(background, (0, 0))
    fenetre.blit(leftSquare, (95, 175))
    fenetre.blit(rightSquare, (735, 175))

def isStartButtonClicked(pos):
    button = [((windowWidth - btnWidth) // 2, (windowHeight - btnHeight) // 2),
              (((windowWidth - btnWidth) // 2)+btnWidth, ((windowHeight - btnHeight) // 2)+btnHeight)]
    return (button[0][0] <= pos[0] <= button[1][0] and button[0][1] <= pos[1] <= button[1][1])

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
                print(f"col={x} row={y}")
                return y,x, (offset==0)

    return None

def main():
    
    fenetre = pygame.display.set_mode((windowWidth, windowHeight))
    
    run = []
    leftGrid = finalGrid
    rightGrid = [[1,2,3],[4,5,6],[7,8,9]]
    
    running = True
    status = "waiting" #running - finished
    
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())
    background.fill(BLUE)
    
    leftSquare = pygame.Surface((450,450))
    leftSquare.fill(WHITE)
    
    rightSquare = pygame.Surface((450,450))
    rightSquare.fill(WHITE)
    
    whiteBG = pygame.Surface((btnWidth,btnHeight))
    whiteBG.fill(YELLOW)
    text = font.render(" Start Game ", True, YELLOW, BLACK)
    textRect = text.get_rect()
    textRect.center = (btnWidth // 2, btnHeight // 2)
    whiteBG.blit(text, textRect)
    startBtn = whiteBG
    startBtnRect = whiteBG.get_rect()
    startBtnRect.center = (windowWidth // 2, windowHeight // 2)
    
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                if status == "playing":
                    analyse = getSquareFromClick(pos)
                    if analyse:
                        processMove(leftGrid,analyse)
                        checkWin(leftGrid,status)
                        
                elif status == "waiting":
                    if isStartButtonClicked(pos):
                        status = "playing"
                        path = Astar.process()
                        leftGrid = path[0]
                        print("start playing")
                        print(leftGrid)
        #----------Drawnings-------
        
        backgrounds(fenetre, background, leftSquare, rightSquare)
        
        pygame.draw.line(fenetre, BLACK, (640,100), (640,700))
        
        if status == "waiting":
            fenetre.blit(startBtn, startBtnRect)
        elif status == "finished":
            pass
            
        #leftSquare.blit(img, (0,0))
        refreshGrid(leftSquare,leftGrid)
        refreshGrid(rightSquare,rightGrid)
        
        
        
        # Rafraîchissement de l'écran toutes les 10ms
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

if __name__ == '__main__':
    main()