#################################################
# Auteurs : Pereira Michel, Tchakalov Miroslav
# Date : 09.01.2021
# Titre : Projet final Pyrat
# Version : 3.0
#################################################

# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here

import math
from AIs.import_resources.calcule_to_path import dijkstra
import time

###############################
# Please put your global variables here


#Class here
################################

class Stock:
    """
    Classe statique pour stocker des informations utiles.
    """
    path_to_cheese: list = []
    taille_cheese_ori:int = 0
    nb_iteration:int = 12
    full_path: list = []

# Function Here
################################


def mouvement(source : tuple, destination : tuple) -> str:
    """
    Cette fonction soustrait la source à la destination qui ne donne une valeur soit positive ou négative en X et Y,
    Ce qui indique la direction dans laquelle la souris doit bouger.

    :param source: Point de départ
    :param destination: Noeud voisin
    :return: La direction du mouvement
    """
    x = int(destination[0] - source[0])
    y = int(destination[1] - source[1])

    direction:tuple = (x, y)

    if direction == (0, -1):
        return MOVE_DOWN
    elif direction == (0, 1):
        return MOVE_UP
    elif direction == (1, 0):
        return MOVE_RIGHT
    elif direction == (-1, 0):
        return MOVE_LEFT


def cheese_proche (distance : list, chesses : list) -> tuple:
    """
    Grâce à la liste des distances, cette fonction repère les coordonnées avec lers distances. Ensuite, cette fonction
    trouve les coordonnées qui ont la plus petite distance. Ainsi, on trouve le fromage le plus proche.

    :param distance: Distances des noeuds dans le labyrinthe depuis le point de départ.
    :param chesses: Liste contenant les coordonnées de tous les fromages dans le labyrinthe.
    :return: Coordonnées du fromage le plus proche.
    """
    distance_chesses : dict = {}

    # Parcourt tous les fromages dans la liste des distances.
    for cheese in chesses:
        distance_chesses[cheese] = distance[cheese]

    min: int = math.inf
    key: tuple

    # Boucle for qui cherche le fromage avec la plus petite distance.
    for plus_petit in distance_chesses.keys():
        if distance_chesses[plus_petit] < min:
            min = distance_chesses[plus_petit]
            key = plus_petit

    return key

def route_chesses (route : dict, cheese : tuple) -> list:
    """
    Cette fonction va tracer un chemin jusqu'au fromage le plus proche.

    :param route: Dictionnaire de noeuds.
    :param cheese: Coordonnées du fromage le plus proche.
    :return: Liste de noeuds à parcourir pour arriver au fromage le plus proche.
    """

    path: list = []

    # Cette boucle va parcourir le chemin depuis le fromage jusqu'a la position de départ qui a un prédecesseur nul
    while cheese != None:
        path.append(cheese)
        cheese = route[cheese]
    return path

################################


###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    """
    Cette fonction se lance qu'une fois au début du programme. Va chercher le chemin le plus cours pour la moitié
    des fromages sur la carte. Stocke également les chemins dans une liste à deux dimmensions. Cette liste sera
    ensuite utilisée dans la fonction turn().
    """
    temp = time.time()

    position: tuple = playerLocation
    Stock.taille_cheese_ori = len(piecesOfCheese)

    # Boucle sur la moitié des fromages. Construit la liste des routes pour attraper les fromages en utilisant
    # la technique du voyageur de commerce.
    for k in range((len(piecesOfCheese) // 2), 0, -1):

        (route, distance) = dijkstra(mazeMap, position, k)

        coord_cheese: tuple = cheese_proche(distance, piecesOfCheese)

        position = coord_cheese

        coord_vers_cheese: list = route_chesses(route, coord_cheese)

        piecesOfCheese.remove(coord_cheese)

        Stock.full_path.insert(0, coord_vers_cheese)

    print("temp:", time.time() - temp)
    print("full path size:", len(Stock.full_path))


###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    """
    Choisi le mouvement à faire pour atteindre le prochain fromage
    """
    movement: str

    # Si la moitié des fromages calculés dans le preprocessing ont été déjà pris. La technique du voyageur de commerce
    # sera appliquée avec la totalité du labyrinthe contrairement au preprocessing qui ne fait ça que sur la moitié.
    if len(Stock.full_path) < 1:

        temp = time.time()

        # Si la liste de chemins est vide. Calcule un nouveau chemin vers le fromage le plus proche.
        if len(Stock.path_to_cheese) <= 1:

            (route, distance) = dijkstra(mazeMap, playerLocation, Stock.nb_iteration)

            coord_cheese: tuple = cheese_proche(distance, piecesOfCheese)

            coord_vers_cheese: list = route_chesses(route, coord_cheese)

            Stock.path_to_cheese = coord_vers_cheese

            movement: str = mouvement(Stock.path_to_cheese[len(Stock.path_to_cheese) - 1],
                                      Stock.path_to_cheese[len(Stock.path_to_cheese) - 2])
            Stock.path_to_cheese.pop()

        # Sinon choisi le prochain chemin dans la liste.
        else:

            movement: str = mouvement(Stock.path_to_cheese[len(Stock.path_to_cheese) - 1],
                                      Stock.path_to_cheese[len(Stock.path_to_cheese) - 2])
            Stock.path_to_cheese.pop()

        print("temp:", time.time() - temp)

    # Si la liste fournie par le preprocessing n'est pas vide, on choisi le prochain chemin dans la liste.
    else:

        # Choisi le chemin à parcourir.
        if len(Stock.path_to_cheese) <= 1:
            Stock.path_to_cheese = Stock.full_path.pop()

        movement: str = mouvement(Stock.path_to_cheese[len(Stock.path_to_cheese) - 1],
                                  Stock.path_to_cheese[len(Stock.path_to_cheese) - 2])
        Stock.path_to_cheese.pop()

    return movement

