from colors import YELLOW,BLACK
import window
import pygame

WIDTH = 450
HEIGHT = 100

pygame.init()

#Police d'ecriture du bouton
fontTitle = pygame.font.Font('freesansbold.ttf', 72)

#Bouton central pour (re)lancer une partie  
#Constitué d'un texte jaune sur un rectangle noir lui meme sur un rectangle jaune plus grand
#pour créer l'effet de bordure  
yellowBG = pygame.Surface((WIDTH,HEIGHT))
yellowBG.fill(YELLOW)
text = fontTitle.render(" Start Game ", True, YELLOW, BLACK)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)
yellowBG.blit(text, textRect)
content = yellowBG # exported
rect = yellowBG.get_rect() # exported
rect.center = (window.WIDTH // 2, window.HEIGHT // 2)

#Position du bouton sur la fenetre (centré)
POSITION = [((window.WIDTH - WIDTH) // 2, (window.HEIGHT - HEIGHT) // 2),
              (((window.WIDTH - WIDTH) // 2)+WIDTH, ((window.HEIGHT - HEIGHT) // 2)+HEIGHT)]

#Retourne si les coordonnée d'un clic correspondent à celles du bouton
def isClicked(pos):
    return (POSITION[0][0] <= pos[0] <= POSITION[1][0] and POSITION[0][1] <= pos[1] <= POSITION[1][1])

pygame.quit()