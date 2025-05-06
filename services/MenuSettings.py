# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath


# -------------- CLASSE DU MENU DES PARAMETRES --------------#
class MenuSettings:
    # -------------- FONCTION D'INITIALISATION --------------#
    pygame.mixer.init()

    def __init__(self, game_status: GameStatus, langue: Langue, theme: Theme, volume: float):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue
        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))
        self.__volume = volume
        self.__old_volume = 0

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontButton(20)
            self.__theme.setSizeFontTitle(50)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontButton(33)
            self.__theme.setSizeFontTitle(90)
        # ------- Définition des variables les plus utilisées -------#
        # ------- Les couleurs : -------#

        # ------- Les objets qui utilisent la couleur : -------#
        self.__title_color = self.__theme.getColorP()
        self.__theme_color = self.__theme.getColorS()
        self.__classic_color = self.__theme.getColorS()
        self.__arcade_color = self.__theme.getColorS()
        self.__horror_color = self.__theme.getColorS()
        self.__language_color = self.__theme.getColorS()
        self.__english_color = self.__theme.getColorS()
        self.__french_color = self.__theme.getColorS()
        self.__volume_color = self.__theme.getColorS()
        self.__barre_color = (200, 200, 200)
        self.__selection_color = self.__theme.getColorP()
        self.__arret_color = (150, 150, 150)
        self.__validate_color = self.__theme.getColorS()
        self.__mute_color = self.__theme.getColorS()
        self.__checkbox_color = self.__theme.getColorP()

        # ------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

        # ------- Initialisation de la fenêtre : -------#
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        # ------- Le titre de la fenêtre et son logo : -------#
        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        # ------- Les polices : -------#
        self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont1()}"), self.__theme.getSizeFontTitle())
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontButton())

        # ------- Les cases à cocher : -------#
        self.__checkbox1 = False
        self.__checkbox2 = False
        self.__checkbox_volume = False
        self.__checkbox4 = False
        self.__checkbox5 = False

        # ------- La valeur des cases à cocher et le fait qu'elle change de couleur en fonction : -------#
        # ------- Check-box des thèmes : -------#
        if self.__theme.getName() == 'Classic':
            self.__checkbox1 = True
        if self.__theme.getName() == 'Arcade':
            self.__checkbox2 = True

        # ------- Check-box des langues : -------#
        if self.__langue.getName() == 'english':
            self.__checkbox4 = True
        if self.__langue.getName() == 'french':
            self.__checkbox5 = True
        # ------- Check-box du volume : -------#
        if self.__volume == 0:
            self.__checkbox_volume = True

        # ------- Définition des polices/positions des titres des check-box : -------#
        self.__title_text = self.__title_font.render(self.__langue.getText1MenuSettings(), True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect(center=(self.__screen_width // 2, 100))

        if self.__langue.getName() == "english" :
            self.__theme_text = self.__element_font.render(f"{self.__langue.getText3MenuSettings()} :", True,
                                                           self.__theme_color)
            self.__theme_text_rect = self.__theme_text.get_rect(topleft=(25, 210))

            self.__classic_text = self.__element_font.render(self.__langue.getText4MenuSettings(), True,
                                                             self.__classic_color)
            self.__classic_text_rect = self.__classic_text.get_rect(topleft=(205, 210))

            self.__arcade_text = self.__element_font.render(self.__langue.getText5MenuSettings(), True, self.__arcade_color)
            self.__arcade_text_rect = self.__arcade_text.get_rect(topleft=(380, 210))

            self.__language_text = self.__element_font.render(f"{self.__langue.getText2MenuSettings()} :", True,
                                                              self.__language_color)
            self.__language_text_rect = self.__language_text.get_rect(topleft=(25, 410))

            self.__english_text = self.__element_font.render(self.__langue.getText7MenuSettings(), True,
                                                             self.__english_color)
            self.__english_text_rect = self.__english_text.get_rect(topleft=(265, 410))

            self.__french_text = self.__element_font.render(self.__langue.getText8MenuSettings(), True, self.__french_color)
            self.__french_text_rect = self.__french_text.get_rect(topleft=(440, 410))

            self.__volume_text = self.__element_font.render(self.__langue.getText10MenuSettings(), True, self.__volume_color)
            self.__volume_text_rect = self.__volume_text.get_rect(topleft=(25, 310))

            self.__mute_text = self.__element_font.render(self.__langue.getText11MenuSettings(), True, self.__mute_color)
            self.__mute_text_rect = self.__mute_text.get_rect(topleft=(555, 310))

            if self.__theme.getName() == "Arcade":
                self.__checkbox1_rect = pygame.Rect(180, 210, 20, 20)
                self.__checkbox2_rect = pygame.Rect(355, 210, 20, 20)
                self.__checkbox4_rect = pygame.Rect(240, 410, 20, 20)
                self.__checkbox5_rect = pygame.Rect(415, 410, 20, 20)
                self.__checkbox_volume_rect = pygame.Rect(530, 310, 20, 20)
            elif self.__theme.getName() == "Classic":
                self.__checkbox1_rect = pygame.Rect(180, 220, 20, 20)
                self.__checkbox2_rect = pygame.Rect(355, 220, 20, 20)
                self.__checkbox4_rect = pygame.Rect(240, 420, 20, 20)
                self.__checkbox5_rect = pygame.Rect(415, 420, 20, 20)
                self.__checkbox_volume_rect = pygame.Rect(530, 320, 20, 20)

        elif self.__langue.getName() == "french":
            self.__theme_text = self.__element_font.render(f"{self.__langue.getText3MenuSettings()} :", True,
                                                           self.__theme_color)
            self.__theme_text_rect = self.__theme_text.get_rect(topleft=(25, 210))

            self.__classic_text = self.__element_font.render(self.__langue.getText4MenuSettings(), True,
                                                             self.__classic_color)
            self.__classic_text_rect = self.__classic_text.get_rect(topleft=(205, 210))

            self.__arcade_text = self.__element_font.render(self.__langue.getText5MenuSettings(), True,
                                                            self.__arcade_color)
            self.__arcade_text_rect = self.__arcade_text.get_rect(topleft=(420, 210))

            self.__language_text = self.__element_font.render(f"{self.__langue.getText2MenuSettings()} :", True,
                                                              self.__language_color)
            self.__language_text_rect = self.__language_text.get_rect(topleft=(25, 410))

            self.__english_text = self.__element_font.render(self.__langue.getText7MenuSettings(), True,
                                                             self.__english_color)
            self.__english_text_rect = self.__english_text.get_rect(topleft=(230, 410))

            self.__french_text = self.__element_font.render(self.__langue.getText8MenuSettings(), True,
                                                            self.__french_color)
            self.__french_text_rect = self.__french_text.get_rect(topleft=(405, 410))

            self.__volume_text = self.__element_font.render(self.__langue.getText10MenuSettings(), True,
                                                            self.__volume_color)
            self.__volume_text_rect = self.__volume_text.get_rect(topleft=(25, 310))

            self.__mute_text = self.__element_font.render(self.__langue.getText11MenuSettings(), True,
                                                          self.__mute_color)
            self.__mute_text_rect = self.__mute_text.get_rect(topleft=(555, 310))

            if self.__theme.getName() == "Arcade":
                self.__checkbox1_rect = pygame.Rect(180, 210, 20, 20)
                self.__checkbox2_rect = pygame.Rect(395, 210, 20, 20)
                self.__checkbox4_rect = pygame.Rect(205, 410, 20, 20)
                self.__checkbox5_rect = pygame.Rect(380, 410, 20, 20)
                self.__checkbox_volume_rect = pygame.Rect(530, 310, 20, 20)
            elif self.__theme.getName() == "Classic":
                self.__checkbox1_rect = pygame.Rect(180, 220, 20, 20)
                self.__checkbox2_rect = pygame.Rect(395, 220, 20, 20)
                self.__checkbox4_rect = pygame.Rect(205, 420, 20, 20)
                self.__checkbox5_rect = pygame.Rect(380, 420, 20, 20)
                self.__checkbox_volume_rect = pygame.Rect(530, 320, 20, 20)

        self.__x = 180
        if self.__theme.getName() == "Arcade":
            self.__y = 305
        elif self.__theme.getName() == "Classic":
            self.__y = 315
        self.__barre_longueur = 300
        self.__barre_hauteur = 30
        self.__espacement = self.__barre_longueur // 10

        # ------- Bouton "valider" : -------#
        self.__validate = pygame.Rect(270, 600, 160, 50)
        self.__validate_text = self.__element_font.render(self.__langue.getText9MenuSettings(), True, self.__validate_color)
        self.__validate_text_rect = self.__validate_text.get_rect()
        self.__validate_text_rect.center = (self.__validate.centerx, self.__validate.centery)

        # -------------- FONCTION D'AFFICHAGE --------------#

    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

        # ------- Affichage du titre -------#
        self.__screen.blit(self.__title_text, self.__title_text_rect)

        # ------- Affichage des noms des check-box -------#
        self.__screen.blit(self.__theme_text, self.__theme_text_rect)
        self.__screen.blit(self.__classic_text, self.__classic_text_rect)
        self.__screen.blit(self.__arcade_text, self.__arcade_text_rect)
        self.__screen.blit(self.__language_text, self.__language_text_rect)
        self.__screen.blit(self.__english_text, self.__english_text_rect)
        self.__screen.blit(self.__french_text, self.__french_text_rect)

        # ------- Affichage des check-box -------#
        pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox1_rect, 2)
        pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox2_rect, 2)
        pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox_volume_rect, 2)
        pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox4_rect, 2)
        pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox5_rect, 2)

        # ------- Affichage des conditions des checkbox pour leur changement de valeur/couleur -------#
        if self.__checkbox1:
            pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox1_rect)
        if self.__checkbox2:
            pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox2_rect)
        if self.__checkbox_volume:
            pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox_volume_rect)
        if self.__checkbox4:
            pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox4_rect)
        if self.__checkbox5:
            pygame.draw.rect(self.__screen, self.__checkbox_color, self.__checkbox5_rect)


        # ------- Affichage du volume -------#
        self.__screen.blit(self.__volume_text, self.__volume_text_rect)
        self.__screen.blit(self.__mute_text, self.__mute_text_rect)

        pygame.draw.rect(self.__screen, self.__barre_color,
                         (self.__x, self.__y, self.__barre_longueur, self.__barre_hauteur))
        pygame.draw.rect(self.__screen, self.__selection_color,
                         (self.__x, self.__y, self.__volume * self.__barre_longueur, self.__barre_hauteur))

        for i in range(11):
            x = self.__x + i * self.__espacement
            pygame.draw.line(self.__screen, self.__arret_color, (x, self.__y + 5),
                             (x, self.__y + self.__barre_hauteur - 5))

        # ------- Affichage du bouton "valider" -------#
        self.__screen.blit(self.__validate_text, self.__validate_text_rect)

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
                    souris_x, souris_y = pygame.mouse.get_pos()
                    if self.__checkbox1_rect.collidepoint(mouse_pos):
                        if self.__checkbox2:
                            self.__checkbox2 = False
                        self.__checkbox1 = not self.__checkbox1
                        self.__theme = Theme("Classic", (111, 66, 25), (0, 0, 0), 90, 65, "KATANA.ttf", "Gamejot.ttf",
                                             "classicTheme.png", "classicTheme2.png", "classicFR.png", "classicENG.png", "flower.png", "mushroom.png",
                                             "butterfly.png",
                                             "leaf.png", (215, 149, 51), (111, 66, 25), (191, 113, 34),
                                             (46, 27, 10),
                                             "classic.mp3")

                    elif self.__checkbox2_rect.collidepoint(mouse_pos):
                        if self.__checkbox1:
                            self.__checkbox1 = False
                        self.__checkbox2 = not self.__checkbox2
                        self.__theme = Theme("Arcade", (55, 57, 144), (0, 0, 0), 60, 35, "ARCADE_I.TTF", "ARCADE_N.TTF",
                                             "arcadeTheme.png", "arcadeTheme4.png", "arcadeFR.png", "arcadeENG.png", "etoile.png", "heart.png",
                                             "clover.png",
                                             "musicNote.png", (196, 254, 255), (55, 57, 144), (155, 201, 201),
                                             (200, 200, 200),
                                             "arcade.mp3")
                    elif (self.__x <= souris_x <= self.__x + self.__barre_longueur and
                          self.__y <= souris_y <= self.__y + self.__barre_hauteur):
                        if self.__checkbox_volume:
                            self.__checkbox_volume = not self.__checkbox_volume
                        arret = (souris_x - (self.__x - 30)) // self.__espacement
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
                    elif self.__checkbox4_rect.collidepoint(mouse_pos):
                        if self.__checkbox5:
                            self.__checkbox5 = False
                        self.__checkbox4 = not self.__checkbox4
                        self.__langue = Langue("english")
                    elif self.__checkbox5_rect.collidepoint(mouse_pos):
                        if self.__checkbox4:
                            self.__checkbox4 = False
                        self.__checkbox5 = not self.__checkbox5
                        self.__langue = Langue("french")

                    elif self.__validate.collidepoint(mouse_pos):
                        self.__game_status.settings_to_principal()
                        return self.__langue, self.__theme, self.__volume

                elif event.type == pygame.MOUSEMOTION:
                    souris_x, souris_y = pygame.mouse.get_pos()
                    mouse_pos = pygame.mouse.get_pos()
                    if self.__checkbox1_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__checkbox2_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__checkbox4_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.__validate.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        self.__validate_color = self.__theme.getColorP()
                    elif self.__checkbox_volume_rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif (self.__x <= souris_x <= self.__x + self.__barre_longueur and
                          self.__y <= souris_y <= self.__y + self.__barre_hauteur):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        self.__validate_color = self.__theme.getColorS()
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.display()
