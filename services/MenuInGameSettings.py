# ---------------- imports --------------------
import pygame
import sys

# Entities
from entities.Players import Players

# Services
from services.PickleHandler import PickleHandler
from services.ResourcePath import resourcePath

# ValueObjects
from valueobjects.Board import Board
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme


# -------------- CLASSE QUI AFFICHE LES PARAMETRES DE JEU --------------#
class MenuInGameSettings:
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue, volume: float, board: Board,
                 players: Players, time: int):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__volume = volume
        self.__old_volume = 0
        self.__board = board
        self.__players = players
        self.__error = ""
        self.__time = time
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(25)
            self.__theme.setSizeFontTitle(50)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(35)
            self.__theme.setSizeFontTitle(80)

        # ------- Les couleurs : -------#
        self.__white = (255, 255, 255)
        self.__black = (0, 0, 0)
        self.__red = (255, 0, 0)
        self.__fleche_color = self.__theme.getColorS()
        self.__volume_color = self.__theme.getColorS()
        self.__barre_color = (200, 200, 200)
        self.__selection_color = self.__theme.getColorP()
        self.__arret_color = (150, 150, 150)
        self.__validate_color = self.__theme.getColorS()
        self.__title_color = self.__theme.getColorP()
        self.__volume_button_color = self.__theme.getColorS()
        self.__restart_button_color = self.__theme.getColorS()
        self.__quit_button_color = self.__theme.getColorS()
        self.__placeholder_color = (200, 200, 200)
        self.__validate_color = self.__theme.getColorS()

        self.__rayon_button = 12

        self.__screen_width = 700
        self.__screen_height = 700

        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        # ------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont1()}"), self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())
        self.__font_error = pygame.font.Font(None, 40)

        self.__title_text = self.__title_font.render(self.__langue.getText1MenuSettingsGame(), True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect()
        self.__title_text_rect.center = (350, 100)

        # def volume
        self.__volume_x = 100
        self.__volume_y = 225
        self.__barre_longueur = 300
        self.__barre_hauteur = 30
        self.__espacement = self.__barre_longueur // 10
        self.__volume_text = self.__element_font.render("Volume", True, self.__volume_color)
        self.__volume_text_rect = self.__volume_text.get_rect(center=(self.__screen_width // 2, 200))

        self.__restart_button = pygame.Rect(215, 500, 275, 50)
        self.__quit_button = pygame.Rect(215, 575, 275, 50)

        # def mute
        self.__mute_text = self.__element_font.render(self.__langue.getText11MenuSettings(), True, self.__black)
        self.__mute_text_rect = self.__mute_text.get_rect(center=(530, self.__volume_y + 15))

        self.__checkbox_volume_rect = pygame.Rect(450, self.__volume_y + 5, 20, 20)
        self.__checkbox_volume = False
        if self.__volume == 0:
            self.__checkbox_volume = True

        # ------- Définition des valeurs de l'encadré -------#
        self.__square_width = self.__screen_width - 20
        self.__square_height = 350
        self.__square_position = (10, 325)
        self.__square = pygame.Rect(self.__square_position, (self.__square_width, self.__square_height))

        # ------- Valeur de la zone de texte mise à zéro -------#
        self.__insert_text = ""
        self.__active_input = False

        # ------- Définition du placeholder de la zone de texte -------#
        self.__text_placeholder = self.__element_font.render(self.__langue.getText3MenuLoadGame(), True, self.__placeholder_color)

        # ------- Définition du titre de l'encadré -------#
        self.__square_title = self.__element_font.render(self.__langue.getText2MenuSettingsGame(), True, self.__black)
        self.__square_title_rect = self.__square_title.get_rect(
            center=(350, 300))

        # ------- Définition de la position de la zone de texte -------#
        self.__text_box = pygame.Rect(50, 325, 600, 50)

        # ------- Définition du bouton "valider" -------#
        position = (self.__screen_width // 2, self.__screen_height // 2 + 100)
        self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True, self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect(center=position)

        # ------- Définition de la fléche "retour" : -------#
        self.__size = 25
        self.__fleche_x = self.__size + 50
        self.__fleche_y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__fleche_x - self.__size, self.__fleche_y - self.__size, 2 * self.__size,
                                    2 * self.__size)

    # ------------ FONCTION D'AFFICHAGE ------------ #
    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))
        self.__screen.blit(self.__title_text, self.__title_text_rect)

        restart_text = self.__button_font.render(self.__langue.getText3MenuSettingsGame(), True, self.__restart_button_color)
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (self.__restart_button.centerx, self.__restart_button.centery)

        quit_text = self.__button_font.render(self.__langue.getText4MenuSettingsGame(), True, self.__quit_button_color)
        quit_text_rect = quit_text.get_rect()
        quit_text_rect.center = (self.__quit_button.centerx, self.__quit_button.centery)

        # affichage volume
        self.__screen.blit(self.__volume_text, self.__volume_text_rect)
        pygame.draw.rect(self.__screen, self.__barre_color,
                         (self.__volume_x, self.__volume_y, self.__barre_longueur, self.__barre_hauteur))
        pygame.draw.rect(self.__screen, self.__selection_color,
                         (self.__volume_x, self.__volume_y, self.__volume * self.__barre_longueur,
                          self.__barre_hauteur))

        for i in range(11):
            x = self.__volume_x + i * self.__espacement
            pygame.draw.line(self.__screen, self.__arret_color, (x, self.__volume_y + 5),
                             (x, self.__volume_y + self.__barre_hauteur - 5))

        self.__screen.blit(restart_text, restart_text_rect)
        self.__screen.blit(quit_text, quit_text_rect)

        # affichage mute
        pygame.draw.rect(self.__screen, self.__theme.getColorP(), self.__checkbox_volume_rect, 2)
        self.__screen.blit(self.__mute_text, self.__mute_text_rect)
        if self.__checkbox_volume:
            pygame.draw.rect(self.__screen, self.__theme.getColorP(), self.__checkbox_volume_rect)

        # ------- Affichage du titre save -------#
        self.__screen.blit(self.__square_title, self.__square_title_rect)

        # affichage message d'erreur / réussite:
        self.__error_display = self.__font_error.render(self.__error, True, self.__red)
        self.__error_display_rect = self.__error_display.get_rect(
            center=(self.__screen_width // 2, self.__screen_height - self.__square_height + 45))
        self.__screen.blit(self.__error_display, self.__error_display_rect)

        # ------- Affichage de la zone de texte, avec ses animations -------#
        pygame.draw.rect(self.__screen, self.__white, self.__text_box, border_radius=self.__rayon_button)
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

        # ------- Affichage du bouton "valider" -------#
        position = (self.__screen_width // 2, self.__screen_height // 2 + 100)
        self.__validate_text = self.__element_font.render(self.__langue.getText7MenuSettingsGame(), True, self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect(center=position)
        self.__screen.blit(self.__validate_text, self.__validate_text_rect)

        # ------- Affichage de la flèche "retour" -------#
        pygame.draw.polygon(self.__screen, self.__fleche_color,
                            [(self.__fleche_x - self.__size, self.__fleche_y),
                             (self.__fleche_x, self.__fleche_y + self.__size),
                             (self.__fleche_x, self.__fleche_y + self.__size // 2),
                             (self.__fleche_x + self.__size, self.__fleche_y + self.__size // 2),
                             (self.__fleche_x + self.__size, self.__fleche_y - self.__size // 2),
                             (self.__fleche_x, self.__fleche_y - self.__size // 2),
                             (self.__fleche_x, self.__fleche_y - self.__size)])
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    souris_x, souris_y = pygame.mouse.get_pos()
                    if (self.__volume_x <= souris_x <= self.__volume_x + self.__barre_longueur and
                            self.__volume_y <= souris_y <= self.__volume_y + self.__barre_hauteur):
                        if self.__checkbox_volume:
                            self.__checkbox_volume = not self.__checkbox_volume
                        arret = (souris_x - (self.__volume_x - 30)) // self.__espacement
                        self.__volume = arret / 10.0
                        pygame.mixer.music.set_volume(self.__volume)
                    elif self.__checkbox_volume_rect.collidepoint(mouse_pos):
                        if not self.__checkbox_volume:
                            self.__old_volume = self.__volume
                            self.__volume = 0
                        else:
                            self.__volume = self.__old_volume
                        pygame.mixer.music.set_volume(self.__volume)
                        self.__checkbox_volume = not self.__checkbox_volume

                    elif self.__text_box.collidepoint(event.pos):
                        self.__active_input = True

                    elif self.__validate_text_rect.collidepoint(mouse_pos) and self.__insert_text != "":
                        self.save()

                    elif self.__restart_button.collidepoint(mouse_pos):
                        self.restart()
                        return self.__theme, self.__langue, self.__volume

                    elif self.__quit_button.collidepoint(mouse_pos):
                        self.__game_status.menu_ingame_settings_to_principal()
                        return self.__theme, self.__langue, self.__volume

                    elif self.__fleche.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_ingame_settings":
                            self.__game_status.menu_ingame_settings_to_game()
                        elif self.__game_status.current_state.id == "menu_ingame_settings_server":
                            self.__game_status.menu_ingame_settings_server_to_game_server()
                        elif self.__game_status.current_state.id == "menu_ingame_settings_client":
                            self.__game_status.menu_ingame_settings_client_to_game_client()
                        return self.__theme, self.__langue, self.__volume
                    else:
                        self.__active_input = False

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    souris_x, souris_y = pygame.mouse.get_pos()
                    if self.__restart_button.collidepoint(mouse_pos):
                        self.__restart_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__quit_button.collidepoint(mouse_pos):
                        self.__quit_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__validate_text_rect.collidepoint(mouse_pos):
                        self.__validate_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__checkbox_volume_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif (self.__volume_x <= souris_x <= self.__volume_x + self.__barre_longueur and
                            self.__volume_y <= souris_y <= self.__volume_y + self.__barre_hauteur):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__restart_button_color = self.__theme.getColorS()
                        self.__validate_color = self.__theme.getColorS()
                        self.__quit_button_color = self.__theme.getColorS()
                        self.__fleche_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.KEYDOWN:
                    # Si la zone de texte est cliquée, alors le placeholder laisse place à la saisie de l'utilisateur.
                    if self.__active_input:
                        if event.key == pygame.K_BACKSPACE:
                            self.__insert_text = self.__insert_text[:-1]
                        else:
                            self.__insert_text += event.unicode
            self.display()

    def save(self):
        # appeler le sys de sauvegarde
        pickle_handler = PickleHandler(self.__insert_text)
        is_done = pickle_handler.save(self.__board, self.__players, self.__time)
        if is_done == True:
            self.__error = self.__langue.getText5MenuSettingsGame()
        else:
            self.__error = self.__langue.getText6MenuSettingsGame()

    def restart(self):
        self.__game_status.menu_ingame_settings_to_restart()
        return

