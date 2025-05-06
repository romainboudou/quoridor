# ---------------- imports --------------------
import pygame
import sys

# Services
from services.PickleHandler import PickleHandler
from services.ResourcePath import resourcePath

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme
from valueobjects.Board import Board

# Entities
from entities.Players import Players


                    #-------------- CLASSE DU MENU DE CHARGEMENT DE PARTIE --------------#
class MenuLoad:
                    # -------------- FONCTION D'INITIALISATION --------------#
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(25)
            self.__theme.setSizeFontTitle(33)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(35)
            self.__theme.setSizeFontTitle(70)
# ------- Définition des variables les plus utilisées -------#
# Les couleurs :
        self.__white = (255, 255, 255)
        self.__red = (255, 0, 0)
        self.__title_color = self.__theme.getColorP()
        self.__text_color = self.__theme.getColorS()
        self.__fleche_color = self.__theme.getColorS()
        self.__placeholder_color = (200, 200, 200)
        self.__validate_color = self.__theme.getColorS()

# Les dimensions de la fenêtre
        self.__screen_width = 700
        self.__screen_height = 700

# ------- Valeur de la zone de texte mise à zéro -------#
        self.__insert_text = ""
        self.__error = ""
        self.__error_text = ""
        self.__active_input = False

# ------- Fonts -------#
        self.__title_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont1()}'),
                                             self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'),
                                              self.__theme.getSizeFontButton())
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())


# ------- Définition du placeholder de la zone de texte -------#
        self.__text_placeholder = self.__button_font.render(self.__langue.getText3MenuLoadGame(), True, self.__placeholder_color)

# ------ Définition du titre pour la zone de texte ------#
        self.__save = self.__button_font.render(self.__langue.getText2MenuLoadGame(), True, self.__text_color)
        self.__save_rect = self.__save.get_rect(center=(self.__screen_width // 2, 350))

#------- Définition des paramètres de la fenêtre -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

#------- Défintion du titre du menu -------#
        self.__text_title = self.__title_font.render(self.__langue.getText1MenuLoadGame(), True, self.__title_color)
        self.__text_title_rect = self.__text_title.get_rect(center=(self.__screen_width // 2, 125))

#------- Définition de la position de la zone de texte -------#
        self.__text_box = pygame.Rect(50, 425, 600, 50)

# ------- Définition de l'erreur -------#
        self.__position_error = (self.__screen_width // 2, 400)
        self.__error_text_display = self.__button_font.render(self.__error_text, True, self.__red)
        self.__error_text_display_rect = self.__error_text_display.get_rect(center=self.__position_error)

# ------- Définition du bouton "valider" -------#
        position = (self.__screen_width // 2, self.__screen_height // 2 + 200)
        self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True,
                                                   self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect(center=position)

#------- Définition de la flèche "retour" -------#
        self.__size = 25
        self.__x = self.__size + 50
        self.__y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

                    #-------------- FONCTION D'AFFICHAGE --------------#
    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

#------- Affichage du titre -------#
        self.__screen.blit(self.__text_title, self.__text_title_rect)

#------ Afichage du sous titre ------#
        self.__screen.blit(self.__save, self.__save_rect)

#------- Affichage de la zone de texte, avec ses animations -------#
        pygame.draw.rect(self.__screen, self.__white, self.__text_box, border_radius=12)
        if self.__theme.getName() == "Arcade":
            if not self.__active_input and self.__insert_text == "":
                self.__screen.blit(self.__text_placeholder, (self.__text_box.x + 45, self.__text_box.y + 15))
            else:
                insert_text_surface = self.__button_font.render(self.__insert_text, True, self.__title_color)
                self.__screen.blit(insert_text_surface, (self.__text_box.x + 45, self.__text_box.y + 15))
        elif self.__theme.getName() == "Classic":
            if not self.__active_input and self.__insert_text == "":
                self.__screen.blit(self.__text_placeholder, (self.__text_box.x + 45, self.__text_box.y + 5))
            else:
                insert_text_surface = self.__button_font.render(self.__insert_text, True, self.__title_color)
                self.__screen.blit(insert_text_surface, (self.__text_box.x + 45, self.__text_box.y + 5))

#------- Affichage de l'erreur -------#
        self.__error_text_display = self.__button_font.render(self.__error_text, True, self.__red)
        self.__error_text_display_rect = self.__error_text_display.get_rect(center=(self.__screen_width //2, 400))
        self.__screen.blit(self.__error_text_display, self.__error_text_display_rect)

# ------- Affichage du bouton "valider" -------#
        position = (self.__screen_width // 2, self.__screen_height // 2 + 200)
        self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True, self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect(center=position)
        self.__screen.blit(self.__validate_text, self.__validate_text_rect)

#------- Affichage de la flèche "retour" -------#
        pygame.draw.polygon(self.__screen, self.__fleche_color,
                            [(self.__x - self.__size, self.__y), (self.__x, self.__y + self.__size),
                             (self.__x, self.__y + self.__size // 2),
                             (self.__x + self.__size, self.__y + self.__size // 2),
                             (self.__x + self.__size, self.__y - self.__size // 2),
                             (self.__x, self.__y - self.__size // 2), (self.__x, self.__y - self.__size)])
        pygame.display.flip()

                    # -------------- FONCTION-BOUCLE DE MENU --------------#
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__text_box.collidepoint(event.pos):
                        self.__active_input = True
                    elif self.__validate_text_rect.collidepoint(mouse_pos) and self.__insert_text != "":
                        self.__error, board, players, time = self.load()
                        self.__insert_text = ""

                        if self.__error == "":
                            # changement game status
                            self.__game_status.menu_load_to_menu_mod_load()
                            return board, players, time
                        else:
                            self.__error_text = self.__langue.getText4MenuLoadGame()
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__game_status.load_to_principal()
                        return 0, 0, 0
                    else:
                        self.__active_input = False
                    #appeler page de chargement vers la classe Serveur
                elif event.type == pygame.KEYDOWN:
# Si la zone de texte est cliquée, alors le placeholder laisse place à la saisie de l'utilisateur.
                    if self.__active_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.__insert_text = self.__insert_text[:-1]
                        else:
                            self.__insert_text += event.unicode
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__text_box.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    elif self.__validate_text_rect.collidepoint(mouse_pos):
                        self.__validate_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__fleche_color = self.__theme.getColorS()
                        self.__validate_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.display()

    def load(self) -> (str, Board, Players, int):
        # appeler le sys de sauvegarde
        pickle_handler = PickleHandler(self.__insert_text)
        error, board, players, time = pickle_handler.load()
        return error, board, players, time
