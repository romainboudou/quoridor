# ---------------- imports --------------------
import pygame

# valueobjects
from valueobjects.Board import Board
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Entities
from entities.Players import Players

# services
from services.ResourcePath import resourcePath


# -------------- CLASSE QUI AFFICHE LA PAGE DE JEU --------------#
class Display:
    def __init__(self, board: Board, screen, theme: Theme, langue: Langue, players: Players):
        self.__board = board
        self.__theme = theme
        self.__langue = langue
        self.__players = players
        self.__player_list = players.getplayerliste()
        self.__size = self.__board.getSize()

        # pygame
        self.__screen = screen

        # ------- Les dimensions de la fenêtre : -------#
        self.__screen_width = 700
        self.__screen_height = 700

        # colors
        self.__black = (0, 0, 0)
        self.__choice_color = self.__theme.getColorChoice()
        self.__case_color = self.__theme.getColorCase()
        self.__wall_color = self.__theme.getColorWall()
        self.__wall_color_init = self.__theme.getColorBoard()
        self.__info_color = self.__black
        self.__settings_button_color = self.__theme.getColorS()
        self.__black = self.__theme.getColorS()

        # fonts
        self.__title_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'),
                                             self.__theme.getSizeFontTitle())
        self.__element_font = pygame.font.Font(resourcePath(f"Repository/fonts/{self.__theme.getFont2()}"),
                                               self.__theme.getSizeFontButton())
        self.__button_font = pygame.font.Font(resourcePath(f'Repository/fonts/{self.__theme.getFont2()}'),
                                              self.__theme.getSizeFontButton())
        self.__font = pygame.font.Font(None, 60)

        # variables affichage pygame
        if self.__size == 5:
            self.__case_size = 52
            self.__wall_size = 10
        elif self.__size == 7:
            self.__case_size = 36
            self.__wall_size = 8
        elif self.__size == 9:
            self.__case_size = 28
            self.__wall_size = 6
        elif self.__size == 11:
            self.__case_size = 20
            self.__wall_size = 8

        self.__affichage_wall_size_of_case = 52
        self.__size_wall_display_player = (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case)
        self.__case_plus_wall = self.__case_size + self.__wall_size
        self.__offset = 200

        # définition des images des joueurs et scale pour qu'elles soient à la bonne taille
        self.__player1 = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagePlayer1()}"))
        self.__player2 = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagePlayer2()}"))
        self.__player3 = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagePlayer3()}"))
        self.__player4 = pygame.image.load(resourcePath(f"Repository/images/{self.__theme.getImagePlayer4()}"))

        self.__image_player1 = pygame.transform.scale(self.__player1, (self.__case_size, self.__case_size))
        self.__image_player2 = pygame.transform.scale(self.__player2, (self.__case_size, self.__case_size))
        self.__image_player3 = pygame.transform.scale(self.__player3, (self.__case_size, self.__case_size))
        self.__image_player4 = pygame.transform.scale(self.__player4, (self.__case_size, self.__case_size))

        self.__image_player1_for_wall = pygame.transform.scale(self.__player1, (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case))
        self.__image_player2_for_wall = pygame.transform.scale(self.__player2, (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case))
        self.__image_player3_for_wall = pygame.transform.scale(self.__player3, (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case))
        self.__image_player4_for_wall = pygame.transform.scale(self.__player4, (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case))

        # définition des variables pour la gestion du texte murs/walls
        self.__walls_text = self.__element_font.render(self.__langue.getText1Game(), True,
                                                 self.__black)
        self.__walls_text_rect = self.__walls_text.get_rect(center=(90, 200))

        # définition pour l'affichage de current/actuel (joueur)
        position = (self.__screen_width // 2 - 50, 150)
        self.__current_player_text = self.__element_font.render(f'{self.__langue.getText2Game()}:', True, self.__black)
        self.__current_player_text_rect = self.__current_player_text.get_rect(center=position)

# -------------- Définition bouton "?" = tooltip --------------#
        position = (625, 75)
        self.__info_text = self.__title_font.render("?", True, self.__info_color)
        self.__info_text_rect = self.__info_text.get_rect(center=position)

# -------------- Affichage bouton settings --------------#
        position = (625, 600)
        self.__wheel = pygame.image.load(resourcePath(f"Repository/images/setting_logo.png"))
        self.__wheel_scale = pygame.transform.scale(self.__wheel, self.__size_wall_display_player)
        self.__wheel_rect = self.__wheel_scale.get_rect(center=position)

    def getCaseSize(self):
        return self.__case_size

    def getCasePlusWall(self):
        return self.__case_plus_wall

    def getOffset(self):
        return self.__offset

    # -------------- Fonction d'affichage principale --------------#
    def displayBoard(self, total_seconds: int, board):

# -------------- TIMER --------------#
        seconds = total_seconds
        seconds = seconds % (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        output_string = "%02d:%02d:%02d" % (hours, minutes, seconds)

# -------------- création variable pour l'affichage du timer --------------#
        text_timer = self.__font.render(output_string, True, self.__wall_color_init)
        text_timer_rect = text_timer.get_rect()
        text_timer_rect.center = (350, 100)

# -------------- surface pour cacher l'horloge de la seconde d'avant --------------#
        surf_hidding_timer = pygame.Surface(text_timer_rect.size)
        surf_hidding_timer.fill(self.__case_color)
        self.__screen.blit(surf_hidding_timer, text_timer_rect)

# -------------- affichage timer --------------#
        self.__screen.blit(text_timer, text_timer_rect)

# -------------- affichage du joueur qui est en train de jouer (image) --------------#
        current_player_id = self.__players.getCurrentPlayer().getId()
        current_player_path = ""
        if current_player_id == 1:
            current_player_path = f"Repository/images/{self.__theme.getImagePlayer1()}"
        elif current_player_id == 2:
            current_player_path = f"Repository/images/{self.__theme.getImagePlayer2()}"
        elif current_player_id == 3:
            current_player_path = f"Repository/images/{self.__theme.getImagePlayer3()}"
        elif current_player_id == 4:
            current_player_path = f"Repository/images/{self.__theme.getImagePlayer4()}"

        current_player_image = pygame.image.load(resourcePath(current_player_path))
        current_player_image_scale = pygame.transform.scale(current_player_image, (self.__affichage_wall_size_of_case, self.__affichage_wall_size_of_case))
        position = (self.__screen_width // 2 + 75, 150)
        surf_current_player_image = pygame.Surface(self.__size_wall_display_player)
        surf_current_player_image.blit(current_player_image_scale, (0, 0))
        surf_current_player_image_rect = surf_current_player_image.get_rect(center=position)
        self.__screen.blit(surf_current_player_image, surf_current_player_image_rect)

# -------------- Affichage current/actuel --------------#
        self.__screen.blit(self.__current_player_text, self.__current_player_text_rect)

# -------------- Affichage bouton "?" = tooltip --------------#
        self.__screen.blit(self.__info_text, self.__info_text_rect)

# ------- Affichage du bouton "Settings" -------#
        self.__screen.blit(self.__wheel_scale, self.__wheel_rect)

# ------- Affichage du texte murs -------#
        self.__screen.blit(self.__walls_text, self.__walls_text_rect)

# ------- Affichage des murs des joueurs -------#
        # player 1
        position = (50, 250)
        player1 = pygame.Surface(self.__size_wall_display_player)
        player1.blit(self.__image_player1_for_wall, (0, 0))
        player1_rect = player1.get_rect(center=position)
        self.__screen.blit(player1, player1_rect)

        walls_text_player1 = self.__element_font.render(f': {self.__player_list[0].getWallNumber()}', True, self.__black)
        walls_text_player1_rect = walls_text_player1.get_rect(center=(125, 250))
        hidding_surf1 = pygame.Surface(walls_text_player1_rect.size)
        hidding_surf1.fill(self.__case_color)
        self.__screen.blit(hidding_surf1, walls_text_player1_rect)
        self.__screen.blit(walls_text_player1, walls_text_player1_rect)

        # player 2
        position = (50, 300)
        player2 = pygame.Surface(self.__size_wall_display_player)
        player2.blit(self.__image_player2_for_wall, (0, 0))
        player2_rect = player2.get_rect(center=position)
        self.__screen.blit(player2, player2_rect)

        walls_text_player2 = self.__element_font.render(f': {self.__player_list[1].getWallNumber()}', True, self.__black)
        walls_text_player2_rect = walls_text_player2.get_rect(center=(125, 300))
        hidding_surf2 = pygame.Surface(walls_text_player2_rect.size)
        hidding_surf2.fill(self.__case_color)
        self.__screen.blit(hidding_surf2, walls_text_player2_rect)
        self.__screen.blit(walls_text_player2, walls_text_player2_rect)

        if self.__board.getNumberOfPlayers() + self.__board.getNumberOfAi() > 2:
            # player 3
            position = (50, 350)
            player3 = pygame.Surface(self.__size_wall_display_player)
            player3.blit(self.__image_player3_for_wall, (0, 0))
            player3_rect = player3.get_rect(center=position)
            self.__screen.blit(player3, player3_rect)

            walls_text_player3 = self.__element_font.render(f': {self.__player_list[2].getWallNumber()}', True,
                                                            self.__black)
            walls_text_player3_rect = walls_text_player3.get_rect(center=(125, 350))
            hidding_surf3 = pygame.Surface(walls_text_player3_rect.size)
            hidding_surf3.fill(self.__case_color)
            self.__screen.blit(hidding_surf3, walls_text_player3_rect)
            self.__screen.blit(walls_text_player3, walls_text_player3_rect)

            # player 4
            position = (50, 400)
            player4 = pygame.Surface(self.__size_wall_display_player)
            player4.blit(self.__image_player4_for_wall, (0, 0))
            player4_rect = player4.get_rect(center=position)
            self.__screen.blit(player4, player4_rect)

            walls_text_player4 = self.__element_font.render(f': {self.__player_list[3].getWallNumber()}', True,
                                                            self.__black)
            walls_text_player4_rect = walls_text_player4.get_rect(center=(125, 400))
            hidding_surf4 = pygame.Surface(walls_text_player4_rect.size)
            hidding_surf4.fill(self.__case_color)
            self.__screen.blit(hidding_surf4, walls_text_player4_rect)
            self.__screen.blit(walls_text_player4, walls_text_player4_rect)


# ------- Affichage du plateau de jeu -------#
        for i in range((self.__size * 2) - 1):
            for j in range((self.__size * 2) - 1):

                position = (self.__offset + (i // 2) * self.__case_plus_wall,
                            self.__offset + (j // 2) * self.__case_plus_wall)

                # mouvements possibles
                if board[i][j] == 8:
                    poss = pygame.Surface((self.__case_size, self.__case_size))
                    poss.fill(self.__choice_color)
                    self.__screen.blit(poss, position)
                # cases vides
                elif board[i][j] == 0:
                    surf = pygame.Surface((self.__case_size, self.__case_size))
                    surf.fill(self.__case_color)
                    self.__screen.blit(surf, position)

                # joueur 1
                elif board[i][j] == 1:
                    player = pygame.Surface((self.__case_size, self.__case_size))
                    player.blit(self.__image_player1, (0, 0))
                    self.__screen.blit(player, position)

                # joueur 2
                elif board[i][j] == 2:
                    player = pygame.Surface((self.__case_size, self.__case_size))
                    player.blit(self.__image_player2, (0, 0))
                    self.__screen.blit(player, position)

                # joueur 3
                elif board[i][j] == 3:
                    player = pygame.Surface((self.__case_size, self.__case_size))
                    player.blit(self.__image_player3, (0, 0))
                    self.__screen.blit(player, position)

                # joueur 4
                elif board[i][j] == 4:
                    player = pygame.Surface((self.__case_size, self.__case_size))
                    player.blit(self.__image_player4, (0, 0))
                    self.__screen.blit(player, position)

                # intersection de murs
                elif board[i][j] == 'I':
                    surf = pygame.Surface((self.__wall_size, self.__wall_size))
                    surf.fill(self.__wall_color)
                    position = (self.__offset + self.__case_size + self.__case_plus_wall * (i // 2),
                                self.__offset + self.__case_size + self.__case_plus_wall * (j // 2))
                    self.__screen.blit(surf, position)

                # murs horizontaux
                elif board[i][j] == 'H':
                    surf = pygame.Surface((self.__wall_size, self.__case_size))
                    surf.fill(self.__wall_color)
                    position = (self.__offset + self.__case_size + self.__case_plus_wall * (i // 2),
                                self.__offset + self.__case_plus_wall * (j // 2))
                    self.__screen.blit(surf, position)

                # murs verticaux
                elif board[i][j] == 'V':
                    surf = pygame.Surface((self.__case_size, self.__wall_size))
                    surf.fill(self.__wall_color)
                    position = (self.__offset + self.__case_plus_wall * (i // 2),
                                self.__offset + self.__case_size + self.__case_plus_wall * (j // 2))
                    self.__screen.blit(surf, position)

                # pas de murs (affichage de base pour les murs)
                elif board[i][j] == ' ':
                    if i % 2 == 1 and j % 2 == 1:
                        surf = pygame.Surface((self.__wall_size, self.__wall_size))
                        surf.fill(self.__wall_color_init)
                        position = (self.__offset + self.__case_size + self.__case_plus_wall * (i // 2),
                                    self.__offset + self.__case_size + self.__case_plus_wall * (j // 2))
                        self.__screen.blit(surf, position)

                    elif i % 2 == 1 and j % 2 == 0:
                        surf = pygame.Surface((self.__wall_size, self.__case_size))
                        surf.fill(self.__wall_color_init)
                        position = (self.__offset + self.__case_size + self.__case_plus_wall * (i // 2),
                                    self.__offset + self.__case_plus_wall * (j // 2))
                        self.__screen.blit(surf, position)

                    elif i % 2 == 0 and j % 2 == 1:
                        surf = pygame.Surface((self.__case_size, self.__wall_size))
                        surf.fill(self.__wall_color_init)
                        position = (self.__offset + self.__case_plus_wall * (i // 2),
                                    self.__offset + self.__case_size + self.__case_plus_wall * (j // 2))
                        self.__screen.blit(surf, position)

        pygame.display.flip()

        # retour des boutons
        return self.__info_text_rect, self.__wheel_rect
