# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath


                    #-------------- CLASSE DU MENU DE CREATION DE PARTIE --------------#
class MenuNewGame:
# -------------- FONCTION D'INITIALISATION --------------#
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(25)
            self.__theme.setSizeFontTitle(38)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(35)
            self.__theme.setSizeFontTitle(53)

# ------- Définition des variables les plus utilisées -------#
#------- Les couleurs : -------#
        self.__black = (0, 0, 0)

#------- Les objets qui utilisent la couleur : -------#
        self.__bouton_5x5_color = self.__theme.getColorP()
        self.__bouton_7x7_color = self.__black
        self.__bouton_9x9_color = self.__black
        self.__bouton_11x11_color = self.__black
        self.__bouton_2players_color = self.__theme.getColorP()
        self.__bouton_4players_color = self.__black
        self.__bouton_ia_color = self.__black
        self.__bouton_start_color = self.__black
        self.__fleche_color = self.__black

#------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

# ------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

# ------- Valeurs par défaut du plateau : -------#
        self.__size_board = 5
        self.__number_of_players = 2
        self.__number_of_ai = 0

#------- Le titre de la fenêtre et son logo : -------#
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

#------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont1()}"), self.__theme.getSizeFontTitle())
        self.__button_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())
        self.__start_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontTitle())

#------- Texte des titres des colones : -------#
        self.__texte_plateau = self.__title_font.render(self.__langue.getText1MenuNewGame(), True, self.__theme.getColorP())
        self.__texte_joueur = self.__title_font.render(self.__langue.getText2MenuNewGame(), True, self.__theme.getColorP())

#------- Boutons de taille du plateau : -------#
        self.__bouton_5x5 = pygame.Rect(150, 150, 100, 50)
        self.__bouton_7x7 = pygame.Rect(150, 260, 100, 50)
        self.__bouton_9x9 = pygame.Rect(150, 370, 100, 50)
        self.__bouton_11x11 = pygame.Rect(150, 480, 100, 50)

#------- Boutons de choix de joueur : -------#
        self.__bouton_2players = pygame.Rect(450, 150, 100, 50)
        self.__bouton_4players = pygame.Rect(450, 315, 100, 50)
        if self.__game_status.current_state.id == "menu_new_game":
            self.__bouton_ia = pygame.Rect(450, 480, 100, 50)

#------- Bouton de lancement du jeu : -------#
        self.__bouton_start = pygame.Rect(250, 600, 250, 50)

#------- Définition de la fléche "retour" : -------#
        self.__size = 25
        self.__x = self.__size + 50
        self.__y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

                    #-------------- FONCTION D'AFFICHAGE --------------#
    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

#------- Affichage du titre -------#
        self.__screen.blit(self.__texte_plateau, (110, 75))

#------- Affichage du bouton "5x5" -------#
        bouton_5x5_text = self.__button_font.render("5x5", True, self.__bouton_5x5_color)
        bouton_5x5_text_rect = bouton_5x5_text.get_rect()
        bouton_5x5_text_rect.center = (self.__bouton_5x5.centerx, self.__bouton_5x5.centery)
        self.__screen.blit(bouton_5x5_text, bouton_5x5_text_rect)

# ------- Affichage du bouton "7x7" -------#
        bouton_7x7_text = self.__button_font.render("7x7", True, self.__bouton_7x7_color)
        bouton_7x7_text_rect = bouton_7x7_text.get_rect()
        bouton_7x7_text_rect.center = (self.__bouton_7x7.centerx, self.__bouton_7x7.centery)
        self.__screen.blit(bouton_7x7_text, bouton_7x7_text_rect)

# ------- Affichage du bouton "9x9" -------#
        bouton_9x9_text = self.__button_font.render("9x9", True, self.__bouton_9x9_color)
        bouton_9x9_text_rect = bouton_9x9_text.get_rect()
        bouton_9x9_text_rect.center = (self.__bouton_9x9.centerx, self.__bouton_9x9.centery)
        self.__screen.blit(bouton_9x9_text, bouton_9x9_text_rect)

# ------- Affichage du bouton "11x11" -------#
        bouton_11x11_text = self.__button_font.render("11x11", True, self.__bouton_11x11_color)
        bouton_11x11_text_rect = bouton_11x11_text.get_rect()
        bouton_11x11_text_rect.center = (self.__bouton_11x11.centerx, self.__bouton_11x11.centery)
        self.__screen.blit(bouton_11x11_text, bouton_11x11_text_rect)

# ------- Affichage du titre "joueur" -------#
        if self.__langue.getName() == "french":
            self.__screen.blit(self.__texte_joueur, (420, 75))
        elif self.__langue.getName() == "english":
            self.__screen.blit(self.__texte_joueur, (400, 75))

# ------- Affichage du bouton "2 joueurs" -------#
        bouton_2players_text = self.__button_font.render("2", True, self.__bouton_2players_color)
        bouton_2players_text_rect = bouton_2players_text.get_rect()
        bouton_2players_text_rect.center = (self.__bouton_2players.centerx, self.__bouton_2players.centery)
        self.__screen.blit(bouton_2players_text, bouton_2players_text_rect)

# ------- Affichage du bouton "4 joueurs" -------#
        bouton_4players_text = self.__button_font.render("4", True, self.__bouton_4players_color)
        bouton_4players_text_rect = bouton_4players_text.get_rect()
        bouton_4players_text_rect.center = (self.__bouton_4players.centerx, self.__bouton_4players.centery)
        self.__screen.blit(bouton_4players_text, bouton_4players_text_rect)

# ------- Affichage du bouton "IA" -------#
        if self.__game_status.current_state.id == "menu_new_game":
            bouton_ia_text = self.__button_font.render(self.__langue.getText3MenuNewGame(), True, self.__bouton_ia_color)
            bouton_ia_text_rect = bouton_ia_text.get_rect()
            bouton_ia_text_rect.center = (self.__bouton_ia.centerx, self.__bouton_ia.centery)
            self.__screen.blit(bouton_ia_text, bouton_ia_text_rect)

# ------- Affichage du bouton pour lancer la partie en fonction des paramètres choisis -------#
        bouton_start_text = self.__start_font.render(self.__langue.getText4MenuNewGame(), True, self.__bouton_start_color)
        bouton_start_text_rect = bouton_start_text.get_rect()
        bouton_start_text_rect.center = (self.__bouton_start.centerx, self.__bouton_start.centery)
        self.__screen.blit(bouton_start_text, bouton_start_text_rect)

        # ------- Affichage de la flèche "retour" -------#
        pygame.draw.polygon(self.__screen, self.__fleche_color, [(self.__x - self.__size, self.__y), (self.__x, self.__y + self.__size),
                                                       (self.__x, self.__y + self.__size // 2),
                                                       (self.__x + self.__size, self.__y + self.__size // 2),
                                                       (self.__x + self.__size, self.__y - self.__size // 2),
                                                       (self.__x, self.__y - self.__size // 2), (self.__x, self.__y - self.__size)])
        pygame.display.flip()

                    #-------------- FONCTION-BOUCLE DE MENU --------------#
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

                        if self.__bouton_5x5.collidepoint(mouse_pos):
                            self.__bouton_5x5_color = self.__theme.getColorP()
                            self.__bouton_7x7_color = self.__theme.getColorS()
                            self.__bouton_9x9_color = self.__theme.getColorS()
                            self.__bouton_11x11_color = self.__theme.getColorS()
                            self.__size_board = 5

                        elif self.__bouton_7x7.collidepoint(mouse_pos):
                            self.__bouton_7x7_color = self.__theme.getColorP()
                            self.__bouton_5x5_color = self.__theme.getColorS()
                            self.__bouton_9x9_color = self.__theme.getColorS()
                            self.__bouton_11x11_color = self.__theme.getColorS()
                            self.__size_board = 7

                        elif self.__bouton_9x9.collidepoint(mouse_pos):
                            self.__bouton_9x9_color = self.__theme.getColorP()
                            self.__bouton_5x5_color = self.__theme.getColorS()
                            self.__bouton_7x7_color = self.__theme.getColorS()
                            self.__bouton_11x11_color = self.__theme.getColorS()
                            self.__size_board = 9

                        elif self.__bouton_11x11.collidepoint(mouse_pos):
                            self.__bouton_11x11_color = self.__theme.getColorP()
                            self.__bouton_5x5_color = self.__theme.getColorS()
                            self.__bouton_7x7_color = self.__theme.getColorS()
                            self.__bouton_9x9_color = self.__theme.getColorS()
                            self.__size_board = 11

                        elif self.__bouton_2players.collidepoint(mouse_pos):
                            self.__bouton_2players_color = self.__theme.getColorP()
                            self.__bouton_4players_color = self.__theme.getColorS()
                            self.__bouton_ia_color = self.__theme.getColorS()
                            self.__number_of_players = 2
                            self.__number_of_ai = 0

                        elif self.__bouton_4players.collidepoint(mouse_pos):
                            self.__bouton_4players_color = self.__theme.getColorP()
                            self.__bouton_2players_color = self.__theme.getColorS()
                            self.__bouton_ia_color = self.__theme.getColorS()
                            self.__number_of_players = 4
                            self.__number_of_ai = 0

                        elif self.__game_status.current_state.id == "menu_new_game" and self.__bouton_ia.collidepoint(mouse_pos):
                            self.__bouton_ia_color = self.__theme.getColorP()
                            self.__bouton_2players_color = self.__theme.getColorS()
                            self.__bouton_4players_color = self.__theme.getColorS()
                            self.__number_of_players = 1
                            self.__number_of_ai = 1

                        elif self.__bouton_start.collidepoint(mouse_pos):
                            if self.__game_status.current_state.id == "menu_new_game":
                                self.__game_status.newgame_to_game()
                            elif self.__game_status.current_state.id == "menu_new_room":
                                self.__game_status.menu_new_room_to_menu_waiting_serveur()
                            return self.__size_board, self.__number_of_players, self.__number_of_ai

                        elif self.__fleche.collidepoint(mouse_pos):
                            if self.__game_status.current_state.id == "menu_new_game":
                                self.__game_status.newgame_to_mod()
                            elif self.__game_status.current_state.id == "menu_new_room":
                                self.__game_status.new_room_to_client_serveur()
                            return self.__size_board, self.__number_of_players, self.__number_of_ai

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__bouton_5x5.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_7x7.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_9x9.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_11x11.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_2players.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_4players.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__game_status.current_state.id == "menu_new_game" and self.__bouton_ia.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__bouton_start.collidepoint(mouse_pos):
                        self.__bouton_start_color = self.__theme.getColorP()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__fleche.collidepoint(mouse_pos):
                        self.__fleche_color = self.__theme.getColorP()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__bouton_start_color = self.__theme.getColorS()
                        self.__fleche_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.display()
