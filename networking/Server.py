# ---------------- imports --------------------
try:
    import cPickle as pickle
except ImportError:
    import pickle
import socket
from threading import Thread
import time

# ValueObjects
from valueobjects.Board import Board

# Entities
from entities.Players import Players


class ServerClient(Thread):
    # init d'un client
    def __init__(self, ip, port, con):
        Thread.__init__(self)
        self.__ip = ip
        self.__port = port
        self.__con = con

    def init(self, number_of_player, size):
        # fonction d'envoi des premières infos
        self.__con.send(pickle.dumps(number_of_player, pickle.HIGHEST_PROTOCOL))
        time.sleep(2)
        self.__con.send(pickle.dumps(size, pickle.HIGHEST_PROTOCOL))

    def connect(self, number_of_player):
        # envoie le nombre de joueurs connectés
        time.sleep(3)
        self.__con.send(pickle.dumps(number_of_player, pickle.HIGHEST_PROTOCOL))

    def send(self, board) -> None:
        # envoie d'un message quelconque
        self.__con.send(pickle.dumps(board))

    def receive(self):
        # fonction de réception
        return pickle.loads(self.__con.recv(10000))


class Server(Thread):
    def __init__(self, board: Board, number_of_player: int, players: Players):
        # init du coeur du serveur
        Thread.__init__(self)
        self.__board = board
        self.__number_of_player = number_of_player
        self.__player_connected = 1

        self.__players = players
        self.__event = False

        # création du socket d'envoi
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((socket.gethostbyname_ex(socket.gethostname())[-1][-1], 8080))
        self.__mythreads = []


        self.__running = True

    def run(self):
        # connexion des clients
        while self.__player_connected < self.__number_of_player:
            self.__sock.listen(self.__number_of_player-1)
            # connexion entrante acceptée
            (con, (ip, port)) = self.__sock.accept()
            # création de l'object ServerClient
            mythread = ServerClient(ip, port, con)
            # début du thread de l'objet créé
            mythread.start()

            # envoie des premières données importantes
            mythread.init(self.__number_of_player,self.__board.getSize())
            time.sleep(1)
            mythread.init(self.__board.getBoard(), self.__players.getPlayersCoords())
            mythread.send(self.__players.getCurrentPlayer().getId())

            # implémentation de l'objet dans une liste
            self.__mythreads.append(mythread)

            # on parcourt la liste des clients avec envoi du nombre de joueurs connectés
            self.__player_connected += 1
            for thread in self.__mythreads:
                thread.connect(len(self.__mythreads)+1)
        self.__event = True

        # boucle de jeu
        while self.__running:
            # attente de réception d'un message
            self.__board.setBoard(self.__mythreads[self.__players.getCurrentPlayer().getId()-2].receive())
            self.__players.getCurrentPlayer().setPlayerCoords(self.__mythreads[self.__players.getCurrentPlayer().getId()-2].receive())

            # on parcourt la liste des threads pour envoyer à tout les clients le nouveau board et les coordonnées du joueur
            for thread in self.__mythreads:
                if thread != self.__mythreads[self.__players.getCurrentPlayer().getId()-2]:
                    thread.send(self.__board.getBoard())
                    thread.send(self.__players.getCurrentPlayer().getPlayerCoords())

            # vérification si le client a gagner
            self.__board.setWin(self.__board.win(self.__players.getCurrentPlayer().getId()))
            # s'il na pas gagner alors on change de joueur
            if not self.__board.getWin():
                self.__players.changePlayer()
            self.__event = True

    def iPlay(self):
        # quand je joue j'envoie directement les infos à tout les clients
        for thread in self.__mythreads:
            thread.send(self.__board.getBoard())
            thread.send(self.__players.getCurrentPlayer().getPlayerCoords())
            self.__board.setWin(self.__board.win(self.__players.getCurrentPlayer().getId()))


    def getEvent(self):
        # retourne l'event pour savoir où se placer entre le game et le serveur
        return self.__event

    def setEvent(self):
        # change d'état l'event (à False)
        self.__event = False

    def stop(self):
        # permet de stopper le thread
        self.__running = False