# ---------------- imports --------------------
import pygame
import sys
import time as t
import socket

# Valueobjects
from valueobjects.Board import Board
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Network
from networking.Server import Server
from networking.Client import Client

# Services
from services.ResourcePath import resourcePath


# -------------- CLASSE DU MENU D'ATTENTE DES AUTRES JOUEURS --------------#
class Waiting:
    def __init__(self, theme: Theme, langue: Langue, game_status, connection):
        self.__theme = theme
        self.__langue = langue
        self.__connection = connection
        self.__game_status = game_status
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))

# ------ L'adresse ip du server : ------#
        self.__local_ip = ""
        if self.__game_status.current_state.id == "menu_waiting_serveur" or self.__game_status.current_state.id == "menu_waiting_load_serveur":
            self.__local_ip = self.get_local_ip()

#------ Les dimensions de la fenêtre : ------#
        self.__screen_width = 700
        self.__screen_height = 700

#------ Initialisation de la fenêtre : ------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

#------ Les couleurs : ------#
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)
        self.__barre_color = self.__theme.getColorP()

#------ La police : ------#
        if self.__theme.getName() == "Arcade":
            self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"),
                                               20)
        if self.__theme.getName() == "Classic":
            self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"),
                                               30)
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"),
                                               self.__theme.getSizeFontButton())


# ------- Le titre de la fenêtre et son logo : -------#
        pygame.display.set_caption("Loading Bar")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

# ------- Définition pour l'affichage du titre de la page : -------#
        self.__title_text = self.__title_font.render(self.__langue.getText1Waiting(), True,
                                                          self.__black)
        self.__title_text_rect = self.__title_text.get_rect(
            center=(self.__screen_width // 2, 100))

# ------- Définition pour l'affichage de l'adresse ip : -------#
        self.__ip_title_text = self.__element_font.render(self.__langue.getText2Waiting(), True,
                                                    self.__black)
        self.__ip_title_text_rect = self.__ip_title_text.get_rect(
            center=(self.__screen_width // 2, self.__screen_height // 2 - 150))
        self.__ip_text = self.__element_font.render(self.__local_ip, True,
                                                       self.__black)
        self.__ip_text_rect = self.__ip_text.get_rect(center=(self.__screen_width // 2, self.__screen_height // 2 - 100))


# ------- La barre de chargement : -------#
        self.__is_loading_bar_finished = False
        self.__loading = False

        self.__barre_x = self.__screen_width // 2 - 150
        self.__barre_y = self.__screen_height // 2
        self.__barre_largeur = 300
        self.__barre_hauteur = 20

        self.__progression = 0
        self.__progression_max = 100

        self.__texte = "Chargement"
        self.__nombre_points = 0
        self.__delai_affichage = 500  # Délai en millisecondes entre chaque changement de point

    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

        # affichage du titre
        self.__screen.blit(self.__title_text, self.__title_text_rect)

        # affichage de l'adresse ip:
        if self.__local_ip != "":
            self.__screen.blit(self.__ip_title_text, self.__ip_title_text_rect)
            self.__screen.blit(self.__ip_text, self.__ip_text_rect)

        if self.__progression < self.__progression_max and self.__loading:
            self.__progression += 1
            t.sleep(0.05)

        pygame.draw.rect(self.__screen, self.__black, (self.__barre_x, self.__barre_y, self.__barre_largeur, self.__barre_hauteur))
        pygame.draw.rect(
            self.__screen,
            self.__barre_color,
            (self.__barre_x, self.__barre_y, self.__barre_largeur * (self.__progression / self.__progression_max), self.__barre_hauteur))
        pygame.display.flip()

    def run(self):
        while True:
            if self.__progression >= self.__progression_max:
                self.__is_loading_bar_finished = True

            if self.__connection.getEvent():
                # lancer la barre de chargement
                # quand elle est finit mettre is_loading_bar_finished à True
                self.__loading = True

            if self.__is_loading_bar_finished:
                self.changeGameStatus()
                return

            self.display()


    def changeGameStatus(self):
        if self.__game_status.current_state.id == "menu_waiting_client":
            self.__game_status.menu_waiting_client_to_game_client()
        elif self.__game_status.current_state.id == "menu_waiting_serveur":
            self.__game_status.menu_waiting_serveur_to_game_server()
        elif self.__game_status.current_state.id == "menu_waiting_load_serveur":
            self.__game_status.menu_waiting_load_serveur_to_game_server()

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('192.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        finally:
            s.close()
        return ip