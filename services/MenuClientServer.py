# ---------------- imports --------------------
import time
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Network
from networking.Server import Server
from networking.Client import Client

# Services
from services.ResourcePath import resourcePath

# -------------- CLASSE DU MENU QUI PROPOSE D'HEBERGER OU REJOINDRE UNE PARTIE --------------#
class MenuClientServer:
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
            self.__theme.setSizeFontTitle(55)

        # ------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

        # ------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        # ------- Objets qui utilisent la couleur : -------#
        self.__white = (255, 255, 255)
        self.__black = (0, 0, 0)
        self.__red = (255, 0, 0)
        self.__title_color = self.__theme.getColorP()
        self.__placeholder_color = (200, 200, 200)
        self.__crea_button_color = self.__theme.getColorS()
        self.__fleche_color = self.__theme.getColorS()
        self.__validate_color = self.__theme.getColorS()

        # ------- Valeur de la zone de texte mise à zéro -------#
        self.__insert_text = ""
        self.__error_text = ""
        self.__active_input = False

        # ------- Le titre de la fenêtre et son logo : -------#
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        # ------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont1()}'), self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'), self.__theme.getSizeFontButton())
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())

        self.__title_text = self.__title_font.render(self.__langue.getText1MenuClientServeur(), True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect()
        self.__title_text_rect.center = (350, 125)

        self.__crea_button = pygame.Rect(215, 250, 275, 50)

        self.__invit_text = self.__button_font.render(self.__langue.getText3MenuClientServeur(), True, self.__black)
        self.__invit_text_rect = self.__invit_text.get_rect()
        self.__invit_text_rect.center = (360, 455)

        self.__text_box = pygame.Rect(50, 505, 600, 50)
        self.__text_placeholder = self.__button_font.render(self.__langue.getText4MenuClientServeur(), True,
                                                           self.__placeholder_color)

        # ------- Définition de l'erreur -------#
        self.__position_error = (self.__screen_width // 2, self.__screen_height - 125)
        self.__error_text_display = self.__button_font.render(self.__error_text, True, self.__red)
        self.__error_text_display_rect = self.__error_text_display.get_rect(center=self.__position_error)

        # ------- Bouton "valider" : -------#
        self.__position_validate = (self.__screen_width // 2, self.__screen_height - 100)
        self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True,
                                                          self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect(center=self.__position_validate)

        # ------- Définition de la flèche "retour" -------#
        self.__size = 25
        self.__x = self.__size + 50
        self.__y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

        self.__screen.blit(self.__title_text, self.__title_text_rect)

        crea_text = self.__button_font.render(self.__langue.getText2MenuClientServeur(), True, self.__crea_button_color)
        crea_text_rect = crea_text.get_rect()
        crea_text_rect.center = (self.__crea_button.centerx, self.__crea_button.centery)
        self.__screen.blit(crea_text, crea_text_rect)

        # ------- Affichage de la zone de texte, avec ses animations -------#
        if self.__game_status.current_state.id == 'menu_client_serveur':
            self.__screen.blit(self.__invit_text, self.__invit_text_rect)
            pygame.draw.rect(self.__screen, self.__white, self.__text_box, border_radius=12)
            if self.__theme.getName() == "Arcade":
                if not self.__active_input and self.__insert_text == "":
                    self.__screen.blit(self.__text_placeholder, (self.__text_box.x + 45, self.__text_box.y + 15))
                else:
                    insert_text_surface = self.__button_font.render(self.__insert_text, True, self.__theme.getColorP())
                    self.__screen.blit(insert_text_surface, (self.__text_box.x + 45, self.__text_box.y + 15))
            elif self.__theme.getName() == "Classic":
                if not self.__active_input and self.__insert_text == "":
                    self.__screen.blit(self.__text_placeholder, (self.__text_box.x + 45, self.__text_box.y + 5))
                else:
                    insert_text_surface = self.__button_font.render(self.__insert_text, True, self.__theme.getColorP())
                    self.__screen.blit(insert_text_surface, (self.__text_box.x + 45, self.__text_box.y + 5))

            # ------- Affichage du bouton "valider" -------#
            self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True, self.__validate_color)
            self.__validate_text_rect = self.__validate_text.get_rect(center=self.__position_validate)
            self.__screen.blit(self.__validate_text, self.__validate_text_rect)

            # ------- Affichage de l'erreur -------#
            self.__error_text_display = self.__button_font.render(self.__error_text, True, self.__red)
            self.__error_text_display_rect = self.__error_text_display.get_rect(center=(self.__screen_width // 2, 400))
            self.__screen.blit(self.__error_text_display, self.__error_text_display_rect)

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
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__crea_button.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_client_serveur":
                            self.__game_status.client_serveur_to_new_room()
                        elif self.__game_status.current_state.id == "menu_client_serveur_load":
                            self.__game_status.menu_client_serveur_load_to_menu_waiting_load_serveur()
                        return 0, 0

                    elif self.__text_box.collidepoint(mouse_pos):
                        self.__active_input = True

                    elif self.__validate_text_rect.collidepoint(mouse_pos) and self.__insert_text != "":
                        client = Client(ip=self.__insert_text, langue=self.__langue, theme=self.__theme)

                        if client.getConnected():
                            client.start()
                            self.__game_status.menu_client_serveur_to_menu_waiting_client()
                            return client
                        else:
                            self.__error_text = self.__langue.getText5MenuClientServeur()

                    elif self.__fleche.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_client_serveur":
                            self.__game_status.clientserveur_to_mod()
                        elif self.__game_status.current_state.id == "menu_client_serveur_load":
                            self.__game_status.menu_client_serveur_load_to_mod_load()
                        return 0, 0
                    else:
                        self.__active_input = False

                elif event.type == pygame.KEYDOWN:
                    # Si la zone de texte est cliquée, alors le placeholder laisse place à la saisie de l'utilisateur.
                    if self.__active_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.__insert_text = self.__insert_text[:-1]
                        else:
                            self.__insert_text += event.unicode

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__crea_button.collidepoint(mouse_pos):
                        self.__crea_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__text_box.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    elif self.__validate_text_rect.collidepoint(mouse_pos):
                        self.__validate_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__crea_button_color = self.__theme.getColorS()
                        self.__validate_color = self.__theme.getColorS()
                        self.__fleche_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.display()

    def new_room(self):
        self.__game_status.client_serveur_to_new_room()

