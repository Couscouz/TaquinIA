import pygame

pygame.init()

#Recuperer chacune des 9 parties du logo Paularis pour les stocker dans une liste d'images
#afin d'y acceder facilement plus tard
allParts = []
for i in range(1,10):
    temp = pygame.image.load(f"img/{i}.jpg")
    allParts.append(pygame.transform.scale(temp, (150,150)))
    
pygame.quit()