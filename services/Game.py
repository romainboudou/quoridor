# ---------------- imports --------------------
import copy
import threading
import time as t
import sys

# network
from networking import Server
from networking import Client

# services
from services.Display import Display
from services.ResourcePath import resourcePath

# valueobjects
from valueobjects.Board import Board
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# entities
from entities.Players import Players
from entities.Ai import Ai

# pygame
import pygame
from pygame.locals import (
    MOUSEBUTTONDOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# -------------- CLASSE DE GESTION DU JEU --------------#
class Game:
    def __init__(self,
                 game_status: GameStatus,
                 board: Board,
                 players: Players,
                 theme: Theme,
                 langue: Langue,
                 time: int,
                 rank: int = 0,
                 server: Server or Client = None):


        self.__game_status = game_status
        self.__board = board
        self.__players = players
        self.__theme = theme
        self.__langue = langue
        self.__rank = rank
        self.__server = server
        self.__size = board.getSize()
        # gestion du temps
        if time != 0:
            self.__frame_count = time
        else:
            self.__frame_count = 0
        self.__frame_rate = 30
        self.__time = self.__frame_count // self.__frame_rate

        # pygame
        # affichage du background, nom de la fenêtre et icon de la fenêtre
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))
        pygame.display.set_caption('Quoridor')
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        self.__screen_size = (700, 700)
        self.__screen = pygame.display.set_mode(self.__screen_size)
        self.__screen.fill((0, 0, 0))

        # init Display (objet)
        self.__display = Display(board, self.__screen, self.__theme, self.__langue, self.__players)

        # variables players
        self.__number_of_players = self.__board.getNumberOfPlayers()
        self.__number_of_ai = self.__board.getNumberOfAi()
        self.__wall_direction = 0
        self.__surface_player = pygame.Surface(self.__screen_size)

        # variables display
        self.__case_size = self.__display.getCaseSize()
        self.__case_plus_wall = self.__display.getCasePlusWall()
        self.__offset = self.__display.getOffset()

        # boutons (redéfini plus tard avec la classe Display)
        self.__info_button = None
        self.__settings_button = None

    # fonction de jeu principale
    def gameLoop(self) -> (str, int):
        self.__screen.blit(self.__background_image, (0, 0))
        clock = pygame.time.Clock()
        running = True
        # on affiche les mouvements possibles pour le premier joueur et on affiche la page de jeu
        self.__board.possible(self.__players.getCurrentPlayer().getPlayerCoords())
        self.__info_button, self.__settings_button = self.__display.displayBoard(self.__time, self.__board.getBoard())

        while running:
            # gestion timer
            self.__time = self.__frame_count // self.__frame_rate

            # quel joueur est en train de jouer ?
            # le jeux est en multijoueur, et est-ce ton tours ?
            # le joueur est humain ?
            if self.__players.getCurrentPlayer().getTypeOfPlayer() == "human":
                if (self.__game_status.current_state.id != "game_client" and
                    self.__game_status.current_state.id != "game_server") \
                        or self.__rank == self.__players.getCurrentPlayer().getId():
                    for event in pygame.event.get():
                        # pour quitter le jeu
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                pygame.display.quit()
                                pygame.quit()
                                sys.exit()
                        elif event.type == QUIT:
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
                        # Quand la souris bouge
                        elif event.type == pygame.MOUSEMOTION:
                            mouse_pos = pygame.mouse.get_pos()
                            if self.__info_button.collidepoint(mouse_pos):
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            elif self.__settings_button.collidepoint(mouse_pos):
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            else:
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        # Quand le joueur clique
                        elif event.type == MOUSEBUTTONDOWN:
                            # touche pour changer la direction des murs (clique droit)
                            if event.button == 3:
                                self.wallChangeDirection()
                            # clique gauche
                            elif event.button == 1:
                                mouse_pos = pygame.mouse.get_pos()
                                # si on clique sur le bouton tooltip/ info (?)
                                if self.__info_button.collidepoint(mouse_pos):
                                    if self.__game_status.current_state.id == 'game':
                                        self.__game_status.game_to_tooltip()
                                    elif self.__game_status.current_state.id == 'game_client':
                                        self.__game_status.game_client_to_tooltip_client()
                                    elif self.__game_status.current_state.id == 'game_server':
                                        self.__game_status.game_server_to_tooltip_server()
                                    # return "nom du gagnant", timer
                                    return "", self.__frame_count

                                # si on clique sur settings/ engrennage
                                elif self.__settings_button.collidepoint(mouse_pos):
                                    if self.__game_status.current_state.id == 'game':
                                        self.__game_status.game_to_menu_ingame_settings()
                                    elif self.__game_status.current_state.id == 'game_client':
                                        self.__game_status.game_client_to_menu_ingame_settings_client()
                                    elif self.__game_status.current_state.id == 'game_server':
                                        self.__game_status.game_server_to_menu_ingame_settings_server()
                                    # return "nom du gagnant", timer
                                    return "", self.__frame_count

                                # on vérifie qu'on clique sur le board:
                                elif (event.pos[0] - self.__offset) < self.__case_plus_wall * self.__size and (
                                        event.pos[1] - self.__offset) < self.__case_plus_wall * self.__size:
                                    # pose de mur
                                    if (event.pos[0] - self.__offset) % self.__case_plus_wall > self.__case_size or (
                                            event.pos[1] - self.__offset) % self.__case_plus_wall > self.__case_size:
                                        x = ((event.pos[0] - self.__offset) // self.__case_plus_wall) * 2
                                        y = ((event.pos[1] - self.__offset) // self.__case_plus_wall) * 2

                                        if self.__board.possibleWall(x, y, self.__board.getBoard(),
                                                                     self.__wall_direction):
                                            board = copy.deepcopy(self.__board.getBoard())
                                            self.__board.putWall(x, y, board, self.__wall_direction)
                                            if self.__board.pathFindingInit(board, self.__players) and self.__players.getWallNumber() > 0:
                                                self.__board.putWall(x, y, self.__board.getBoard(),
                                                                     self.__wall_direction)
                                                # on enlève un mur au joueur
                                                self.__players.removeWallFromPlayer()
                                                # on change de joueur et on re affiche le board
                                                if self.__game_status.current_state.id == "game_client" \
                                                        or self.__game_status.current_state.id == "game_server":
                                                    self.__server.iPlay()
                                                self.__players.changePlayer()

                                    # déplacement du pion
                                    else:
                                        x = ((event.pos[0] - self.__offset) // self.__case_plus_wall) * 2
                                        y = ((event.pos[1] - self.__offset) // self.__case_plus_wall) * 2
                                        if self.__board.possibleMovePawn(x, y):
                                            self.__board.movePawn(x, y, self.__players)
                                            # on envoie les données si on est en multi
                                            if self.__game_status.current_state.id == "game_client" \
                                                    or self.__game_status.current_state.id == "game_server":
                                                self.__server.iPlay()
                                            # on vérififie si le joueur a gagné avant de changer de joueur
                                            if self.__board.win(self.__players.getCurrentPlayer().getId()):
                                                self.win()

                                                return self.__players.getCurrentPlayer().getName(), self.__time
                                            # on change de joueur et on re affiche le board
                                            self.__players.changePlayer()


     

            # si le joueur est une ia
            elif self.__players.getCurrentPlayer().getTypeOfPlayer() == "ai":
                self.__board.removePossible()
                ai = Ai(self.__board, self.__players, self.__number_of_players)
                ai.play()
                # on vérififie si le joueur a gagné avant de changer de joueur
                if self.__board.win(self.__players.getCurrentPlayer().getId()):
                    self.win()
                    return self.__players.getCurrentPlayer().getName(), self.__time
                self.__players.changePlayer()

            # on affiche les cases possibles dans le board
            self.__board.possible(self.__players.getCurrentPlayer().getPlayerCoords())
            board = copy.deepcopy(self.__board.getBoard())

            mouse_pos = pygame.mouse.get_pos()

            # affichage des "faux" murs
            if self.__offset < mouse_pos[1] < self.__screen_size[1] - self.__offset \
                    and self.__offset < mouse_pos[0] < self.__screen_size[0] - self.__offset:
                self.__board.putWall((mouse_pos[0] - self.__offset) // self.__case_plus_wall * 2,
                                     (mouse_pos[1] - self.__offset) // self.__case_plus_wall * 2, board,
                                     self.__wall_direction)

            # le joueur a t'il gagné (multi)
            if self.__board.getWin():
                t.sleep(2)
                self.__server.stop()
                self.win()
                return self.__players.getCurrentPlayer().getName(), self.__time

            # update timer
            self.__frame_count += 1
            if self.__time >= 86400:
                self.__time = 0
            clock.tick(self.__frame_rate)

            # appel de la fonction display
            self.__info_button, self.__settings_button = self.__display.displayBoard(self.__time, board)

    # ------------------ FONCTION POUR CHANGER LA DIRECTION DU MUR (horizontal / vertical) ---------------------------#
    def wallChangeDirection(self):
        if self.__wall_direction == 0:  # horizontale
            self.__wall_direction = 1.  # verticale
        else:
            self.__wall_direction = 0

    # ------------------ FONCTION POUR ENVOYER LE(S) JOUEURS VERS MENU-FIN ---------------------------#
    def win(self) -> bool:
        if self.__game_status.current_state.id == 'game':
            self.__game_status.game_to_menu_fin()
        elif self.__game_status.current_state.id == 'game_client':
            self.__game_status.game_client_to_menu_fin()
        elif self.__game_status.current_state.id == 'game_server':
            self.__game_status.game_server_to_menu_fin()

    def getPlayers(self):
        return self.__players

