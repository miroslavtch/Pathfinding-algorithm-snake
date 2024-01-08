#################################################
# Auteurs : Pereira Michel, Tchakalov Miroslav
# Date : 09.01.2021
# Titre : Projet final Pyrat
# Version : 3.0
#################################################
from AIs.import_resources.pqueue import PriorityQueue
import math

def dijkstra(lab: dict, source : tuple, nb_iteration:int) -> tuple:
    """
    L'algorithme Dijkstra nous permet de calculer la distance de chaque noeud depuis le point de départ
    dans le but de trouver chemin le plus court.

    :param lab: Labyrinthe de dictionnaire contenant des noeuds
    :param source: Point de départ
    :param nb_iteration: Nombre de fois qu'on appelle dijkstra
    :return: Liste de routes et leurs distances
    """

    dist: dict = {source: 0}
    route: dict = {}
    q_p: PriorityQueue = PriorityQueue()

    for cordonne in lab:
        if cordonne != source:
            dist[cordonne] = math.inf
        route[cordonne] = None
        q_p.add(cordonne, priority=dist[cordonne])

    cpt: int = 0

    # Cette boucle de parcours va appeller la fonction test() comme condition.
    while not test(q_p, nb_iteration, cpt):
        cord: tuple = q_p.pop()
        voisains: dict = lab[cord[1]]
        for voisin in voisains.keys():
            tmp_dist: int = dist[cord[1]] + voisains[voisin]
            if tmp_dist < dist[voisin]:
                dist[voisin] = tmp_dist
                route[voisin] = cord[1]
                q_p.add(voisin, priority=tmp_dist)
        cpt += 1

    print("cpt:", cpt)

    return (route, dist)


def test(q_p: PriorityQueue, iteration: int, cpt: int) -> bool:
    """

    :param q_p: Arbre prioritaire
    :param iteration: Nombre de fois que Dijkstra à été appelé
    :param cpt: Compteur de boucle while
    :return: Boolean
    """

    # Condition si nombre d'itérations est plus grand que 1 qui retourne le nombre de fois que le programme doit faire la boucle while
    if iteration > 1:
        print("iteration: ", iteration)
        return (q_p.size // iteration) <= cpt

    # retourne si la queue prioritaire est vite, se produit lorsque 50% des fromages les plus proches ont été trouvés
    return q_p.is_empty()




