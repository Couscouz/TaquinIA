#Noeud du graphe principal pour l'algo A*
class TaquinNode:
    #Initialisation d'un noeud suivant une grille
    def __init__(self, grid, p=0, w=0):
        self.grid = grid  # Configuration actuelle du puzzle
        self.previousWeights = p  # Coût du chemin jusqu'à ce nœud
        self.weight = w  # Coût heuristique du nœud à l'objectif
        self.toGetHereWeight = p + w  # Coût total
        self.parent = None  # Noeud parent

    #Définit la comparaison entre 2 noeuds
    def __lt__(self, other):
        return self.toGetHereWeight < other.toGetHereWeight