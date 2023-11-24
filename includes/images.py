import pygame

pygame.init()

img = pygame.image.load("img/PDPPaular.png")
img = pygame.transform.scale(img, (450,450))

allPart = []
for i in range(9):
    temp = pygame.image.load(f"img/{i+1}.jpg")
    allPart.append(pygame.transform.scale(temp, (150,150)))
    
pygame.quit()