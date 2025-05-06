# ---------------- imports --------------------
import pygame
import sys

# Entities
from entities.Players import Players

# Services
from services.Game import Game
from services.MenuFin import MenuFin
from services.MenuInGameSettings import MenuInGameSettings
from services.MenuLoad import MenuLoad
from services.MenuMod import MenuMod
from services.MenuNewGame import MenuNewGame
from services.MenuSettings import MenuSettings
from services.MenuPrincipal import MenuPrincipal
from services.MenuClientServer import MenuClientServer
from services.MenuWaiting import Waiting
from services.Tooltip import Tooltip

# Valueobjects
from valueobjects.Board import Board
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Network
import threading
from networking.Server import Server
from networking.Client import Client

# init pygame
pygame.init()


# -------------- CLASSE DE GESTION DU JEU --------------#
# on retourne içi pour lancer tout les menus ou le jeu
class Start:
    def __init__(self):
        # init du status du jeu
        self.__game_status = GameStatus()
        self.__client = None

        # valeurs par default des différentes variables
        self.__size = 5
        self.__number_of_players = 2
        self.__number_of_ai = 0

        # init theme et langue
        self.__theme = Theme("Classic", (111, 66, 25), (0, 0, 0), 90, 65, "KATANA.ttf", "Gamejot.ttf",
                             "classicTheme.png", "classicTheme2.png", "classicFR.png", "classicENG.png", "flower.png",
                             "mushroom.png",
                             "butterfly.png",
                             "leaf.png", (215, 149, 51), (111, 66, 25), (191, 113, 34),
                             (46, 27, 10),
                             "classic.mp3")
        self.__langue = Langue("english")

        # init time
        self.__time = 0

        # init volume
        self.__volume = 0.5
        pygame.mixer.music.set_volume(self.__volume)

        # init game et winner (str)
        self.__board = None
        self.__players = None
        self.__game = None
        self.__winner = ""

    def mainLoop(self):
        # boucle principale de l'utilisation du jeu
        while True:
            # affichage du menu principal
            if self.__game_status.current_state.id == 'menu_principal':
                menu_principal = MenuPrincipal(self.__game_status, self.__theme, self.__langue)
                self.__langue, self.__theme = menu_principal.run()

                # remise à zéro des variables
                self.__board = None
                self.__players = None
                self.__game = None
                self.__winner = ""

            elif self.__game_status.current_state.id == "menu_new_game":
                menu_new_game = MenuNewGame(self.__game_status, self.__theme, self.__langue)
                self.__size, self.__number_of_players, self.__number_of_ai = menu_new_game.run()
                # creation de l'objet game
                self.__board = Board(self.__size, self.__number_of_players, self.__number_of_ai)
                self.__players = Players(self.__size, self.__number_of_players, self.__number_of_ai, False, self.__theme, self.__langue)
                self.__time = 0
                self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue, self.__time)

            # affichage du menu settings (parametre du jeu: nb de joueurs, taille du plateau)
            elif self.__game_status.current_state.id == 'menu_settings':
                menu_settings = MenuSettings(self.__game_status, self.__langue, self.__theme, self.__volume)
                self.__langue, self.__theme, self.__volume = menu_settings.run()
                # return avec une fonction, les parametre pour creer le board un peu plus loin

            # affichage menu loading
            elif self.__game_status.current_state.id == 'menu_load':
                menu_load = MenuLoad(self.__game_status, self.__theme, self.__langue)
                self.__board, self.__players, self.__time = menu_load.run()

                if type(self.__board) == Board and type(self.__players) == Players and type(self.__time) == int:
                    self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue, self.__time)

            # affichage menu mod
            elif self.__game_status.current_state.id == "menu_mod":
                menu_mod = MenuMod(self.__game_status, self.__theme, self.__langue, self.__game)
                menu_mod.run()

            # affichage menu client serveur
            elif self.__game_status.current_state.id == "menu_client_serveur":
                menu_client_serveur = MenuClientServer(self.__game_status, self.__theme, self.__langue)
                self.__client = menu_client_serveur.run()

            # affichage du jeu
            elif self.__game_status.current_state.id == 'game':
                # affichage du jeu
                self.__winner, self.__time = self.__game.gameLoop()

            elif self.__game_status.current_state.id == 'menu_new_room':
                menu_new_room = MenuNewGame(self.__game_status, self.__theme, self.__langue)
                self.__size, self.__number_of_players, self.__number_of_ai = menu_new_room.run()
                # recreation de l'objet game
                self.__board = Board(self.__size, self.__number_of_players, self.__number_of_ai)
                self.__players = Players(self.__size, self.__number_of_players, self.__number_of_ai, False, self.__theme, self.__langue)
                self.__time = 0

            elif self.__game_status.current_state.id == "menu_fin":
                menu_fin = MenuFin(self.__game_status, self.__theme, self.__langue, self.__winner)
                menu_fin.run()

            elif self.__game_status.current_state.id == "menu_waiting_serveur":
                server = Server(self.__board, self.__number_of_players, self.__players)
                server.start()

                menu_waiting = Waiting(self.__theme, self.__langue, self.__game_status, server)
                menu_waiting.run()
                self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue, 0, 1,server)


            elif self.__game_status.current_state.id == "menu_waiting_client":
                menu_waiting = Waiting(self.__theme, self.__langue, self.__game_status, self.__client)
                menu_waiting.run()

                self.__board = self.__client.getBoard()
                self.__players = self.__client.getPlayer()

                self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue, 0,
                                   self.__client.getRank(), self.__client)

            elif self.__game_status.current_state.id == "menu_waiting_load_serveur":
                self.__number_of_players = self.__board.getNumberOfPlayers()
                server = Server(self.__board, self.__number_of_players, self.__players)
                server.start()

                menu_waiting = Waiting(self.__theme, self.__langue, self.__game_status, server)
                menu_waiting.run()

                self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue, self.__time, 1,
                                   server)

            elif self.__game_status.current_state.id == "menu_ingame_settings":
                menu_ingame_settings = MenuInGameSettings(self.__game_status, self.__theme, self.__langue, self.__volume, self.__board, self.__players, self.__time)
                self.__theme, self.__langue, self.__volume = menu_ingame_settings.run()

            elif self.__game_status.current_state.id == "tooltip":
                tooltip = Tooltip(self.__game_status, self.__theme, self.__langue)
                tooltip.run()

            elif self.__game_status.current_state.id == "game_client":
                self.__winner, self.__time = self.__game.gameLoop()

            elif self.__game_status.current_state.id == "game_server":
                self.__winner, self.__time = self.__game.gameLoop()

            elif self.__game_status.current_state.id == "menu_client_serveur_load":
                menu_client_serveur = MenuClientServer(self.__game_status, self.__theme, self.__langue)
                self.__client = menu_client_serveur.run()

            elif self.__game_status.current_state.id == "menu_mod_load":
                menu_mod = MenuMod(self.__game_status, self.__theme, self.__langue, self.__game)
                menu_mod.run()

            elif self.__game_status.current_state.id == "restart":
                self.__board = Board(self.__size, self.__number_of_players, self.__number_of_ai)
                self.__players = Players(self.__size, self.__number_of_players, self.__number_of_ai, False, self.__theme, self.__langue)
                self.__time = 0
                self.__game = Game(self.__game_status, self.__board, self.__players, self.__theme, self.__langue,self.__time)
                self.__game_status.restart_to_game()
                      