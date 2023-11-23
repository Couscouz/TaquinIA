#from Astar import process
import pygame


pygame.init()
titre = pygame.display.set_caption("Taquin")

clock = pygame.time.Clock()

skyblue = 135,206,235
black = 0,0,0
white = 255,255,255
yellow = 255,255,0

windowHeight = 800
windowWidth = 1280

font = pygame.font.Font('freesansbold.ttf', 72)

img = pygame.image.load("img/PDPPaular.png")
img = pygame.transform.scale(img, (450,450))

allPart = []
for i in range(9):
    temp = pygame.image.load(f"img/{i+1}.jpg")
    allPart.append(pygame.transform.scale(temp, (150,150)))

#---------------------------------------------

def backgrounds(fenetre,background,leftSquare,rightSquare):
    fenetre.blit(background, (0, 0))
    fenetre.blit(leftSquare, (95, 175))
    fenetre.blit(rightSquare, (735, 175))

def getButtonFromClick(pos):
    button1 = [(),()]
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
    
    running = True
    status = "waiting" #running - finished
    
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())
    background.fill(skyblue)
    
    leftSquare = pygame.Surface((450,450))
    leftSquare.fill(white)
    
    rightSquare = pygame.Surface((450,450))
    rightSquare.fill(white)
    
    whiteBG = pygame.Surface((500,200))
    whiteBG.fill(white)
    startButton = font.render("Start Game", True, yellow, black)
    startBtnRect = startButton.get_rect()
    startBtnRect.center = (windowWidth // 2, windowHeight // 2)
    whiteBG.blit(startButton, startBtnRect)
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                if status is "playing":
                    analyse = getSquareFromClick(pos)
                    print(analyse)
                elif status is "waiting":
                    action = getButtonFromClick(pos)

        backgrounds(fenetre, background, leftSquare, rightSquare)
        
        if status is "waiting":
            fenetre.blit(whiteBG, startBtnRect)
            
        #leftSquare.blit(img, (0,0))
        
        index = 0
        for y in [0, 150, 300]:
            for x in [0, 150, 300]:
                if index == 8:
                    break
                leftSquare.blit(allPart[index], (x,y))
                index += 1
        
        pygame.draw.line(fenetre, black, (640,100), (640,700))
        # Rafraîchissement de l'écran toutes les 10ms
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

if __name__ == '__main__':
    main()