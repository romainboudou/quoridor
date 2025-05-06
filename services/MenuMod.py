# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath
from services.Game import Game

                    # -------------- CLASSE DU MENU DE CHOIX LOCAL OU MULTIJOUEUR --------------#
class MenuMod:

                    # -------------- FONCTION D'INITIALISATION --------------#
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue, game: Game):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))
        self.__game = game
        self.__multi = True

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(38)
            self.__theme.setSizeFontTitle(53)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(53)
            self.__theme.setSizeFontTitle(90)

# ------- Définition des variables les plus utilisées -------#
#------- Les couleurs : -------#
        self.__black = (0, 0, 0)

#------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

#------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

#------- Objets qui utilisent la couleur : -------#
        self.__title_color = self.__theme.getColorP()
        self.__solo_button_color = self.__theme.getColorS()
        self.__multi_button_color = self.__theme.getColorS()
        self.__fleche_color = self.__theme.getColorS()

#------- Le titre de la fenêtre et son logo : -------#
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

#------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont1()}'), self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'), self.__theme.getSizeFontButton())

#------- Le titre du menu affiché dans la page : -------#
        self.__title_text = self.__title_font.render(self.__langue.getText1MenuMode(), True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect()
        self.__title_text_rect.center = (350, 150)

#------- Le bouton "LOCAL" : -------#
        self.__solo_button = pygame.Rect(215, 300, 275, 50)

#------- Le bouton "ONLINE" -------#
        self.__multi_button = pygame.Rect(160, 450, 400, 50)

#------- Définition de la flèche "retour" : -------#
        self.__size = 25
        self.__x = self.__size + 50
        self.__y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

        # vérif si c'est une partie contre une ia (cf on ne laisse pas l'utilisateur faire une partie multijoueur)
        if self.__game != None:
            self.__players_liste = self.__game.getPlayers().getplayerliste()

            for player in self.__players_liste:
                if player.getTypeOfPlayer() == 'ai':
                    self.__multi = False

                # -------------- FONCTION D'AFFICHAGE -------------- #
    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))
#------- Affichage du titre -------#
        self.__screen.blit(self.__title_text, self.__title_text_rect)

# ------- Affichage du bouton "LOCAL" -------#
        solo_text = self.__button_font.render(self.__langue.getText2MenuMode(), True, self.__solo_button_color)
        solo_text_rect = solo_text.get_rect()
        solo_text_rect.center = (self.__solo_button.centerx, self.__solo_button.centery)

        self.__screen.blit(solo_text, solo_text_rect)

# ------- Affichage du bouton "ONLINE" -------#
        if self.__multi:
            multi_text = self.__button_font.render(self.__langue.getText3MenuMode(), True, self.__multi_button_color)
            multi_text_rect = multi_text.get_rect()
            multi_text_rect.center = (self.__multi_button.centerx, self.__multi_button.centery)

            self.__screen.blit(multi_text, multi_text_rect)

# ------- Affichage de la flèche "retour" -------#
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
                    if self.__solo_button.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_mod":
                            self.__game_status.mod_to_newgame()
                        elif self.__game_status.current_state.id == "menu_mod_load":
                            self.__game_status.menu_mod_load_to_game()
                        return 0, 0

                    elif self.__multi_button.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_mod":
                            self.__game_status.mod_to_clientserveur()
                        elif self.__game_status.current_state.id == "menu_mod_load":
                            self.__game_status.menu_mod_load_to_menu_client_serveur_load()
                        return 0, 0

                    elif self.__fleche.collidepoint(mouse_pos):
                        if self.__game_status.current_state.id == "menu_mod":
                            self.__game_status.mod_to_principal()
                        elif self.__game_status.current_state.id == "menu_mod_load":
                            self.__game_status.menu_mod_load_to_menu_load()

                        return 0, 0

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__solo_button.collidepoint(mouse_pos):
                        self.__solo_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__multi_button.collidepoint(mouse_pos):
                        self.__multi_button_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__title_color
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__solo_button_color = self.__theme.getColorS()
                        self.__multi_button_color = self.__theme.getColorS()
                        self.__fleche_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.display()
