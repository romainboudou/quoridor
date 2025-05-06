# ---------------- imports --------------------#
import copy
import random

# ValueObjects
from valueobjects.Board import Board

# Entities
from entities.Players import Players

# Services
from services.PathFinding import PathFinding

# Classe contenant l'algorithme de notre intelligence artificielle
class Ai:
    def __init__(self, board: Board, players: Players, nbPlayer):
        self.__players = players
        self.__board = board
        self.__size = self.__board.getSize()
        self.__nbPlayer = nbPlayer

    def play(self):
        played = False
        while not played:
            # l'ia choisit aléatoirement entre la pose d'un mur et le mouvement de son pion
            choice_ia = random.randint(1, 2)
            current_player_pos = self.__players.getCurrentPlayer().getPlayerCoords()
            nb_of_walls = self.__players.getCurrentPlayer().getWallNumber()

            board = copy.deepcopy(self.__board.getBoard())

            # l'ia choisit le mouvement de son pion
            if choice_ia == 1:
                # init du pathfinding
                path_finding = PathFinding(board, self.__size)
                size = self.__board.getSize()
                paths = []

                # position de l'ia
                start = current_player_pos

                # les positions où l'ia doit aller
                targets = []
                target = [0, 0]
                for i in range(size):
                    targets.append(target)
                    target = [0, target[1] + 2]

                # on lance la fonction de recherce de chemin pour chaque target
                for target in targets:
                    path = path_finding.pathFinding(start, target)
                    paths.append(path)
                # on enlève les chemin = None (pas de chemin)
                for i in range(len(paths)):
                    if None in paths:
                        paths.remove(None)

                # si il existe un chemin (vérification pour être sûr)
                if len(paths) > 0:
                    choice = paths[0]
                    # on choisit le chemin le plus court
                    for path in paths:
                        if len(choice) > len(path):
                            choice = path

                    # on choisit x et y qui font du sens
                    if start[0] == choice[1][0] and start[1] == choice[1][1]:
                        x = choice[2][0]
                        y = choice[2][1]
                    else:
                        x = choice[1][0]
                        y = choice[1][1]
                    # on met l'ia à ces coordonnées x et y
                    self.__board.movePawn(x, y, self.__players)
                    played = True

            # l'ia choisit de poser un mur
            else:
                # l'ia a t'elle encore un mur ?
                if nb_of_walls > 0:
                    # on choisit un joueur au hasard (pas important car l'ia se joue contre un seul joueur mais intéressant
                    # si on donnait la possibilté de jouer avec plus de joueurs)
                    player_focus = random.randint(1, self.__nbPlayer)
                    while player_focus == self.__players.getCurrentPlayer().getId():
                        player_focus = random.randint(1, self.__nbPlayer)

                    # mur vertical si joueur 1 ou 2 sinon horizontal
                    if player_focus > 2:
                        wall_direction = 1
                    else:
                        wall_direction = 0

                    # les coordonnées de ce joueur
                    coord = self.__players.getplayerliste()[player_focus - 1].getPlayerCoords()
                    x = coord[0]
                    y = coord[1]

                    if player_focus == 1:
                        x += 1
                    elif player_focus == 2:
                        x -= 1
                    elif player_focus == 3:
                        y += 1
                    elif player_focus == 4:
                        y -= 1

                    # on regarde si on peut poser le mur, si oui on le pose
                    if self.__board.possibleWall(x, y, self.__board.getBoard(), wall_direction):
                        board = copy.deepcopy(self.__board.getBoard())
                        self.__board.putWall(x, y, board, wall_direction)
                        if self.__board.pathFindingInit(board, self.__players) and self.__players.getWallNumber() > 0:
                            self.__board.putWall(x, y, self.__board.getBoard(), wall_direction)
                            self.__players.removeWallFromPlayer()
                            played = True
