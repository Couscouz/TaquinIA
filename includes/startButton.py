import includes.window as window
from colors import YELLOW,BLACK
import pygame

WIDTH = 450
HEIGHT = 100

pygame.init()

fontTitle = pygame.font.Font('freesansbold.ttf', 72)


#Bouton central pour (re)lancer une partie    
yellowBG = pygame.Surface((WIDTH,HEIGHT))
yellowBG.fill(YELLOW)
text = fontTitle.render(" Start Game ", True, YELLOW, BLACK)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)
yellowBG.blit(text, textRect)
content = yellowBG # exported
rect = yellowBG.get_rect() # exported
rect.center = (window.WIDTH // 2, window.HEIGHT // 2)

POSITION = [((window.WIDTH - WIDTH) // 2, (window.HEIGHT - HEIGHT) // 2),
              (((window.WIDTH - WIDTH) // 2)+WIDTH, ((window.HEIGHT - HEIGHT) // 2)+HEIGHT)]

def isClicked(pos):
    return (POSITION[0][0] <= pos[0] <= POSITION[1][0] and POSITION[0][1] <= pos[1] <= POSITION[1][1])

pygame.quit()