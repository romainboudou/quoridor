# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath


# -------------- CLASSE QUI GERE L'AFFICHAGE DES REGLES EN JEU --------------#
class Tooltip:
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue):
        self.__game_status = game_status
        self.__langue = langue
        self.__theme = theme

        # ------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

        # ------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        # ------ Initialisation de l'image comprenant les règles : ------#
        if self.__langue.getName() == "english":
            self.__rules = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getTooltipENG()}"))
        elif self.__langue.getName() == "french":
            self.__rules = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getTooltipFR()}"))
        self.__rules_scale = pygame.transform.scale(self.__rules, (700, 700))

        # ------ On met cette image en image de fond ------#
        # self.__background_image = pygame.image.load(ressourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))
        self.__screen.blit(self.__rules_scale, (0, 0))

        # ------ Les couleurs : ------ #
        self.__black = (0, 0, 0)
        self.__fleche_color = self.__theme.getColorS()

        # rectangle qui a la taille de l'image des rêgles et qui est centré au centre de la fenêtre
        self.__rules_rect = self.__rules.get_rect(
            center=(self.__screen_width // 2, self.__screen_height // 2))

        # ------- Définition de la fléche "retour" : -------#
        self.__size = 25
        self.__x = 30
        self.__y = 30
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

    def display(self):
        # ------ Affichage de l'image des règles : ------ #
        # self.__screen.blit(self.__rules, self.__rules_rect)

        # ------- Affichage de la flèche "retour" -------#
        pygame.draw.polygon(self.__screen, self.__fleche_color,
                            [(self.__x - self.__size, self.__y), (self.__x, self.__y + self.__size),
                             (self.__x, self.__y + self.__size // 2),
                             (self.__x + self.__size, self.__y + self.__size // 2),
                             (self.__x + self.__size, self.__y - self.__size // 2),
                             (self.__x, self.__y - self.__size // 2), (self.__x, self.__y - self.__size)])
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.__fleche.collidepoint(mouse_pos):
                            if self.__game_status.current_state.id == "tooltip":
                                self.__game_status.tooltip_to_game()
                            elif self.__game_status.current_state.id == "tooltip_client":
                                self.__game_status.tooltip_client_to_game_client()
                            elif self.__game_status.current_state.id == "tooltip_server":
                                self.__game_status.tooltip_server_to_game_server()
                            return
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__theme.getColorP()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__fleche_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            self.display()
