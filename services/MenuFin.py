# ---------------- imports --------------------
import pygame
import sys

# ValueObjects
from valueobjects.GameStatus import GameStatus
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Services
from services.ResourcePath import resourcePath

# -------------- CLASSE QUI AFFICHE LA FIN DE PARTIE --------------#
class MenuFin:
    def __init__(self, game_status: GameStatus, theme: Theme, langue: Langue, winner: str):
        self.__game_status = game_status
        self.__theme = theme
        self.__langue = langue

        self.__background_image = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagebg2()}"))

        if self.__theme.getName() == "Arcade":
            self.__theme.setSizeFontTitle(31)
        elif self.__theme.getName() == "Classic":
            self.__theme.setSizeFontTitle(60)

        self.__black = (0, 0, 0)
        self.__title_color = self.__theme.getColorP()
        self.__fleche_color = self.__theme.getColorS()

        self.__screen_width = 700
        self.__screen_height = 700

        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

        pygame.display.set_caption("Quoridor")
        self.__icon = pygame.image.load(resourcePath("Repository/images/icon.png"))
        pygame.display.set_icon(self.__icon)

        self.__title_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"), self.__theme.getSizeFontTitle())

        self.__title_text = self.__title_font.render(f"{winner}{self.__langue.getText1MenuFin()}", True, self.__title_color)
        self.__title_text_rect = self.__title_text.get_rect()
        self.__title_text_rect.center = (350, 350)

        self.__size = 25
        self.__x = self.__size + 50
        self.__y = self.__screen_height - self.__size - 50
        self.__fleche = pygame.Rect(self.__x - self.__size, self.__y - self.__size, 2 * self.__size, 2 * self.__size)

    # -------------- FONCTION D'AFFICHAGE -------------- #
    def display(self):
        self.__screen.blit(self.__background_image, (0, 0))

        self.__screen.blit(self.__title_text, self.__title_text_rect)

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
                    if self.__fleche.collidepoint(mouse_pos):
                        self.__game_status.menu_fin_to_principal()
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
        pass