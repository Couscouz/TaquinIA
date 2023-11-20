from Astar import process
import pygame


pygame.init()
titre = pygame.display.set_caption("Taquin")

clock = pygame.time.Clock()

skyblue = 135,206,235
black = 0,0,0
white = 255,255,255

img = pygame.image.load("img/PDPPaular.png")
img = pygame.transform.scale(img, (450,450))

allPart = []
for i in range(9):
    temp = pygame.image.load(f"img/{i+1}.jpg")
    allPart.append(pygame.transform.scale(temp, (150,150)))

#---------------------------------------------

def main():
    
    fenetre = pygame.display.set_mode((1280, 800))
    
    running = True
    
    # Création d'une image de la taille de la fenêtre
    background = pygame.Surface(fenetre.get_size())
    background.fill(skyblue)
    
    leftSquare = pygame.Surface((450,450))
    leftSquare.fill(white)
    
    rightSquare = pygame.Surface((450,450))
    rightSquare.fill(white)

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fenetre.blit(background, (0, 0))
        fenetre.blit(leftSquare, (95, 175))
        fenetre.blit(rightSquare, (735, 175))
        
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

if __name__ == '__main__':
    main()