from colors import BLUE,BLACK,WHITE
from grid import GOAL_GRID,PLAIN_GRID
from tools import getEmptyPosition,areNeightbours,dim3to1
from Astar import process as AstarGeneration
from images import allParts
import startButton
import window
import pygame


pygame.init()

#2 polices nécessaires (bouton et compteur)
fontTitle = pygame.font.Font('freesansbold.ttf', 72)
fontIndics = pygame.font.Font('freesansbold.ttf', 48)

#Initialisation de la fenetre, du titre et de l'horloge (pour le délai de rafraichissement)
titre = pygame.display.set_caption("Taquin")
fenetre = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
clock = pygame.time.Clock()

#-------------------Surfaces------------------------

#Carré blanc simulant la case vide dans une grille
whiteSquare = pygame.Surface((150,150))
whiteSquare.fill(WHITE)

# Création d'une image de la taille de la fenêtre
background = pygame.Surface(fenetre.get_size())
background.fill(BLUE)

#Surfaces des fonds de taquin
leftSquare = pygame.Surface((450,450))
rightSquare = pygame.Surface((450,450))

#Compteur de coups simulé dans le but de recuperer l'emplacement (moveRect) qui ne sera plus modifié
moveCounter = fontIndics.render(f"Coups joués : 0", True, BLACK)
moveRect = moveCounter.get_rect()
moveRect.center = (window.WIDTH // 2, window.HEIGHT // 8)

joueur = fontIndics.render("Joueur", True, BLACK)
joueurRect = joueur.get_rect()
joueurRect.center = (window.WIDTH // 4, 5 * window.HEIGHT // 6)

ia = fontIndics.render("IA", True, BLACK)
iaRect = ia.get_rect()
iaRect.center = (3 * window.WIDTH // 4, 5 * window.HEIGHT // 6)

#------------------Fonctions-------------------------  

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
                background.blit(allParts[order[index]-1], (x,y))
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
    #Definitions des empalcements des cases sur l'ecran 
    horizontal = [(95,245), (246, 395), (396,545)]
    vertical = [(175,325),(326,475),(476,625)] 
    for y in range(3):
        for x in range(3):
            if ((horizontal[x][0]) < location[0] <= (horizontal[x][1])) and (vertical[y][0] < location[1] <= vertical[y][1]):
                return y,x
    #Si le clic ne correspond à aucune case il vaut None
    return None


def main():
    #Valeur des grille au lancement, les 9 carrés sont bien triés pour un bel affichage avant la 1ere partie
    leftGrid = PLAIN_GRID
    rightGrid = PLAIN_GRID
    
    running = True
    #La partie repose sur 2 status 
    # -> "waiting" quand partie pas en cours (si terminée alors elle est de nouveau en waiting)
    # -> "playing" quand partie en cours
    status = "waiting"
    
    # nb de coups joués dans la partie actuellen et nb de parties jouées
    coups = 0  
    played = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Fermeture classiques
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                #Recuperation du clic de souris
                pos = pygame.mouse.get_pos()
                if status == "playing":
                    #si partie en cours on recupere le possible carré correspondant au clic
                    analyse = getSquareFromClick(pos)
                    if analyse:
                        #si le coups est jouable il est fait et le compteur est incrémenté
                        if processMove(leftGrid, analyse):
                            coups += 1
                            moveCounter = fontIndics.render(f"Coups joués : {coups}", True, BLACK)
                            rightGrid = path[coups]
                        #Verification des conditions de fin de partie
                        sentence = checkWin(leftGrid,rightGrid)
                        if sentence is not None:
                            #si partie terminée on affiche le resultat et retour en phase d'attente (avec bouton)
                            status = "waiting"
                            endMessage,msgRect,played = endGame(played,sentence)     
                        
                elif status == "waiting":
                    if startButton.isClicked(pos):
                        #si phase d'attente et que le bouton start est cliqué, initialisation de la partie (grilles, compteur,solution)
                        status = "playing"
                        path,leftGrid,rightGrid,coups = initGame()
                        moveCounter = fontIndics.render(f"Coups joués : 0", True, BLACK)
        
        #----------Visuels-------
        
        #Superposition des zones de fond
        graphics(fenetre, background, leftSquare, rightSquare)
        
        #Affichages specifiques à la phase actuelle de la partie 
        if status == "waiting":
            #Bouton start si partie en attente
            fenetre.blit(startButton.content, startButton.rect)
            if played > 0:
                #message de fin si partie terminée (simulé par attente et au moins 1 partie jouée)
                fenetre.blit(endMessage, msgRect)
        elif status == "playing":
            #Compteur de coups si partie en cours
            fenetre.blit(moveCounter, moveRect)
            #Indication visuelle sur qui possede quelle grille
            fenetre.blit(joueur, joueurRect)
            fenetre.blit(ia, iaRect)

        #leftSquare.blit(img, (0,0))
        refreshGrid(leftSquare,leftGrid)
        refreshGrid(rightSquare,rightGrid)
        
        # Rafraîchissement de l'écran toutes les 10ms
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

if __name__ == '__main__':
    main()