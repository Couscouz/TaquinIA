#Noeud du graphe principal
class TaquinNode:
    def __init__(self, state, p=0, w=0):
        self.state = state  # Configuration actuelle du puzzle
        self.previousWeights = p  # Coût du chemin jusqu'à ce nœud
        self.weight = w  # Coût heuristique du nœud à l'objectif
        self.toGetHereWeight = p + w  # Coût total
        self.parent = None  # Noeud parent

    def __lt__(self, other):
        return self.toGetHereWeight < other.toGetHereWeight