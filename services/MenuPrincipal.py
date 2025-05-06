# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath


# -------------- CLASSE DU MENU PRINCIPAL --------------#
class MenuPrincipal:
    # -------------- FONCTION D'INITIALISATION --------------#
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg()}"))

        if self.__langue.getName() == "french" and self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(25)
            self.__theme.setSizeFontTitle(60)
        elif self.__langue.getName() == "english" and self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(35)
            self.__theme.setSizeFontTitle(60)
        elif self.__langue.getName() == "french" and self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(40)
            self.__theme.setSizeFontTitle(90)
        elif self.__langue.getName() == "english" and self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(65)
            self.__theme.setSizeFontTitle(90)

        if self.__theme.getName() == "Arcade":
            pygame.mixer.music.load(resourcePath(f"Repository/sons/{self.__theme.getAudio()}"))
            pygame.mixer.music.play(-1)
        elif self.__theme.getName() == "Classic":
            pygame.mixer.music.load(resourcePath(f"Repository/sons/{self.__theme.getAudio()}"))
            pygame.mixer.music.play(-1)

        # ------- Définition des variables les plus utilisées -------#
        # ------- Les couleurs : -------#
        self.__title_color = self.__theme.getColorP()
        self.__newgame_button_color = self.__theme.getColorS()
        self.__loadgame_button_color = self.__theme.getColorS()
        self.__settings_button_color = self.__theme.getColorS()
        self.__black = self.__theme.getColorS()

        # ------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

        # ------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        # ------- Le titre de la fenêtre avec son logo : -------#
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        # ------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont1()}'),
                                             self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'),
                                              self.__theme.getSizeFontButton())

        # ------- Le titre affiché dans la page : -------#
        self.__title_text = self.__title_font.render("Quoridor", True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect()
        self.__title_text_rect.center = (360, 138)

        # ------- Les boutons en fonction de la langue choisie : -------#
        if self.__theme.getName() == "Arcade" and self.__langue.getName() == "english":
            self.__newgame_button = pygame.Rect(225, 325, 275, 50)
            self.__loadgame_button = pygame.Rect(225, 400, 275, 50)
            self.__settings_button = pygame.Rect(225, 475, 275, 50)
        elif self.__theme.getName() == "Arcade" and self.__langue.getName() == "french":
            self.__newgame_button = pygame.Rect(185, 325, 350, 50)
            self.__loadgame_button = pygame.Rect(135, 400, 450, 50)
            self.__settings_button = pygame.Rect(225, 475, 275, 50)
        elif self.__theme.getName() == "Classic" and self.__langue.getName() == "english":
            self.__newgame_button = pygame.Rect(225, 300, 275, 50)
            self.__loadgame_button = pygame.Rect(225, 410, 275, 50)
            self.__settings_button = pygame.Rect(225, 520, 275, 50)
        elif self.__theme.getName() == "Classic" and self.__langue.getName() == "french":
            self.__newgame_button = pygame.Rect(225, 300, 275, 50)
            self.__loadgame_button = pygame.Rect(225, 410, 275, 50)
            self.__settings_button = pygame.Rect(225, 520, 275, 50)

            # -------------- FONCTION D'AFFICHAGE --------------#

    def display(self):
        # ------- Affichage du bouton "New Game" -------#
        new_game_text = self.__button_font.render(self.__langue.getText1MenuPrincipale(), True,
                                                 self.__newgame_button_color)
        new_game_text_rect = new_game_text.get_rect()
        new_game_text_rect.center = (self.__newgame_button.centerx, self.__newgame_button.centery)

        # ------- Affichage du bouton "Load Game" -------#
        load_game_text = self.__button_font.render(self.__langue.getText2MenuPrincipale(), True,
                                                    self.__loadgame_button_color)
        load_game_text_rect = load_game_text.get_rect()
        load_game_text_rect.center = (self.__loadgame_button.centerx, self.__loadgame_button.centery)

        # ------- Affichage du bouton "Settings" -------#
        settings_text = self.__button_font.render(self.__langue.getText3MenuPrincipale(), True,
                                                    self.__settings_button_color)
        settings_text_rect = settings_text.get_rect()
        settings_text_rect.center = (self.__settings_button.centerx, self.__settings_button.centery)

        # ------- Affichage du l'image de fond -------#
        self.__screen.blit(self.__background_image, (0, 0))

        # ------- Affichage du titre du menu -------#
        self.__screen.blit(self.__title_text, self.__title_text_rect)

        # ------- Affichage du texte de chaque bouton -------#
        self.__screen.blit(new_game_text, new_game_text_rect)
        self.__screen.blit(load_game_text, load_game_text_rect)
        self.__screen.blit(settings_text, settings_text_rect)

        pygame.display.flip()

        # -------------- FONCTION-BOUCLE DE MENU --------------#

    def run(self) -> (Langue, Theme):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__newgame_button.collidepoint(mouse_pos):
                        self.__game_status.principal_to_mod()
                        return self.__langue, self.__theme

                    elif self.__loadgame_button.collidepoint(mouse_pos):
                        self.__game_status.principal_to_load()
                        return self.__langue, self.__theme

                    elif self.__settings_button.collidepoint(mouse_pos):
                        self.__game_status.principal_to_settings()
                        return self.__langue, self.__theme

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__newgame_button.collidepoint(mouse_pos):
                        self.__newgame_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__loadgame_button.collidepoint(mouse_pos):
                        self.__loadgame_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__settings_button.collidepoint(mouse_pos):
                        self.__settings_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.__newgame_button_color = self.__black
                        self.__loadgame_button_color = self.__black
                        self.__settings_button_color = self.__black
            self.display()


