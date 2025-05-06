# ---------------- imports --------------------
import socket
import time
try:
    import cPickle as pickle
except ImportError:
    import pickle
from threading import Thread

# Entities
from entities.Players import Players

# ValueObjects
from valueobjects.Board import Board
from valueobjects.Theme import Theme
from valueobjects.Langues import Langue


class Client(Thread):
    def __init__(self, ip: str, langue: Langue, theme: Theme):
        # init d'une connexion client
        Thread.__init__(self)
        self.__ip = ip
        self.__theme = theme
        self.__langue = langue
        self.__port = 8080
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__event = False
        self.__number_of_player_connected = 0
        # Établir la connexion
        self.__connected = False

        # tentative de connexion
        try:
            self.__sock.connect((self.__ip, self.__port))
            # confirmation de la connexion
            self.__connected = True
        except Exception as e:
            # retourne l'erreur s'il y en a une
            print(f"error: {e}")
            self.__connected = False
        self.__running = self.__connected


    def run(self):
        # début du thread
        # récuperation des infos indispensables
        self.__number_of_player = pickle.loads(self.__sock.recv(1032))
        self.__size = pickle.loads(self.__sock.recv(1032))
        self.__board = Board(self.__size, self.__number_of_player, 0)
        self.__players = Players(self.__size, self.__number_of_player, 0, True, self.__theme, self.__langue)
        self.__board.setBoard(pickle.loads(self.__sock.recv(1032)))
        self.__players.setPlayersCoords(pickle.loads(self.__sock.recv(1032)))
        self.__players.setCurrentPlayer(pickle.loads(self.__sock.recv(1032)))

        self.__number_of_player_connected = pickle.loads(self.__sock.recv(1032))
        # affectation du rank du player ( position: 1er/2eme/... joueur à jouer )
        self.__rank = self.__number_of_player_connected

        # attente de tout les joueurs
        while self.__number_of_player > self.__number_of_player_connected:
            self.__number_of_player_connected = pickle.loads(self.__sock.recv(1032))

        self.__event = True

        # début du jeu
        while self.__running:
            # attente de recevoir un message du serveur
            self.__board.setBoard(pickle.loads(self.__sock.recv(4096)))
            self.__players.getCurrentPlayer().setPlayerCoords(pickle.loads(self.__sock.recv(1024)))

            # regarde si le joueur qui a jouer a gagné
            self.__board.setWin(self.__board.win(self.__players.getCurrentPlayer().getId()))

            # s'il na pas gagné on change de joueur
            if not self.__board.getWin():
                self.__players.changePlayer()
            self.__event = True


    def getConnected(self):
        # on regarde si la connexion est ok
        return self.__connected

    def iPlay(self):
        # quand c'est à moi de jouer
        self.__sock.send(pickle.dumps(self.__board.getBoard()))
        self.__sock.send(pickle.dumps(self.__players.getCurrentPlayer().getPlayerCoords()))
        self.__board.setWin(self.__board.win(self.__players.getCurrentPlayer().getId()))

    # Getters les éléments de base du jeu
    def getNumberOfPlayerConnected(self):
        return self.__number_of_player_connected
    
    def getBoard(self):
        return self.__board

    def getPlayer(self):
        return self.__players

    def getRank(self):
        return self.__rank

    def getEvent(self):
        return self.__event

    # Setter de l'event (à False)
    def setEvent(self):
        self.__event = False

    # Stop de la boucle du thread
    def stop(self):
        self.__running = False