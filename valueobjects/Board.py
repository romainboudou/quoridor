# ---------------- imports --------------------
import copy

# Entities
from entities.Players import Players


# -------------- CLASSE QUI GERE LE PLATEAU DE JEU --------------#
class Board:
    def __init__(self, size: int, number_of_player: int, number_of_ai: int):
        self.__size = size
        self.__number_of_player = number_of_player
        self.__number_of_ai = number_of_ai
        self.__board = self.newBoard()
        self.__win = False

    # fonction qui renvoie la taille du plateau
    def getSize(self) -> int:
        return self.__size

    # focntion qui renvoie le nombre de joueur
    def getNumberOfPlayers(self) -> int:
        return self.__number_of_player

    # fonction qui renvoie le nombre d'ia (pour nous, entre 0 et 1 mais qui pourrait être plus, plus tard)
    def getNumberOfAi(self) -> int:
        return self.__number_of_ai

    # fonction qui renvoie le plateau sous forme de liste de listes
    def getBoard(self) -> list:
        return self.__board

    # fonction qui change le plateau dans l'objet board (utilisé pour le jeu en multijoueur)
    def setBoard(self, board: list):
        self.__board = board

    # fonction qui initialise le plateau
    def newBoard(self) -> list:
        board = []
        for i in range((self.__size * 2) - 1):
            board.append([])
            for j in range((self.__size * 2) - 1):
                if i % 2 == 0 and j % 2 == 0:
                    board[i].append(0)
                else:
                    board[i].append(' ')
        # on ajoute içi les différents joueurs sur le plateau
        board[0][self.__size - 1] = 1
        board[-1][self.__size - 1] = 2
        if self.__number_of_player + self.__number_of_ai == 4:
            board[self.__size - 1][0] = 3
            board[self.__size - 1][-1] = 4
        return board

    # fonction qui permet de bouger son pion
    def movePawn(self, x: int, y: int, players: Players):
        # récupération des coordonnées du joueur actuel
        current_player_coords = players.getCurrentPlayer().getPlayerCoords()
        # on ajoute les 8 sur les cases où le joueur peut jouer
        self.possible(current_player_coords)
        # définition du joueur actuel
        current_player = players.getCurrentPlayer()
        # on appelle la fonction qui vérifie si on peut jouer
        if self.possibleMovePawn(x, y):
            # on place le joueur sur le plateau aux coordonnées x, y
            self.__board[x][y] = current_player.getId()
            # on enlève le joueur de ses anciennes coordonnées
            self.__board[current_player_coords[0]][current_player_coords[1]] = 0
            # on redéfini les coordonnées du joueur comme étant les coordonnées x, y où il s'est deplacé
            current_player.setPlayerCoords([x, y])

    # fonction qui vérifie si le joueur peut jouer en (x, y)
    def possibleMovePawn(self, x: int, y: int) -> bool:
        # si les coordonnées x et y sont sur le plateau et que la case contient un 8 (là où on peut jouer)
        # alors on return True, sinon False
        if 0 <= y < (self.__size * 2) - 1 and 0 <= x < (self.__size * 2) - 1 and self.__board[x][y] == 8:
            return True
        return False

    # fonction qui place des "8" sur le plateau là où le joueur peut jouer
    def possible(self, current_player_coords: list[int]):
        # enlève les possibles d'avant
        self.removePossible()
        # recupère les coordonnées
        i = current_player_coords[0]
        j = current_player_coords[1]
        # on test si on peut bouger vers le haut
        # on regarde au dessus de nous si il y a un mur
        if i > 0 and self.__board[i - 1][j] == ' ':
            # si oui si il y a un joueur ?
            if self.__board[i - 2][j] == 0:
                # si il n'y a personne on pose un 8
                self.__board[i - 2][j] = 8
            else:
                # s'il y a une personne on regarde derière ce joueur s'il y a un mur et un joueur derrière
                if i - 2 > 0 and self.__board[i - 3][j] == ' ' and self.__board[i - 4][j] == 0:
                    self.__board[i - 4][j] = 8
                else:
                    # s'il y a un mur, un joueur, ou le bord du plateau on regarde à droite et à gauche du joueur qui est à coté de nous
                    # on regarde à droite
                    if j > 0 and self.__board[i - 2][j - 1] == ' ' and self.__board[i - 2][j - 2] == 0:
                        self.__board[i - 2][j - 2] = 8
                    # puis à gauche
                    if j < self.__size * 2 - 2 and self.__board[i - 2][j + 1] == ' ' and \
                            self.__board[i - 2][j + 2] == 0:
                        self.__board[i - 2][j + 2] = 8

        # pareil en bas
        if i < self.__size * 2 - 2 and self.__board[i + 1][j] == ' ':
            if self.__board[i + 2][j] == 0:
                self.__board[i + 2][j] = 8
            else:
                if i + 2 < self.__size * 2 - 2 and self.__board[i + 3][j] == ' ' and self.__board[i + 4][j] == 0:
                    self.__board[i + 4][j] = 8
                else:
                    if j > 0 and self.__board[i + 2][j - 1] == ' ' and self.__board[i + 2][j - 2] == 0:
                        self.__board[i + 2][j - 2] = 8
                    if j < self.__size * 2 - 2 and self.__board[i - 2][j + 1] == ' ' and \
                            self.__board[i + 2][j + 2] == 0:
                        self.__board[i + 2][j + 2] = 8

        # pareil à gauche
        if j > 0 and self.__board[i][j - 1] == ' ':
            if self.__board[i][j - 2] == 0:
                self.__board[i][j - 2] = 8
            else:
                if j - 2 > 0 and self.__board[i][j - 3] == ' ' and  self.__board[i][j - 4] == 0:
                    self.__board[i][j - 4] = 8
                else:
                    if i > 0 and self.__board[i - 1][j - 2] == ' ' and self.__board[i - 2][j - 2] == 0:
                        self.__board[i - 2][j - 2] = 8
                    if i < self.__size * 2 - 2 and self.__board[i + 1][j - 2] == ' ' and \
                            self.__board[i + 2][j - 2] == 0:
                        self.__board[i + 2][j - 2] = 8

        # puis à droite
        if j < self.__size * 2 - 2 and self.__board[i][j + 1] == ' ':
            if self.__board[i][j + 2] == 0:
                self.__board[i][j + 2] = 8
            else:
                if j + 2 < self.__size * 2 - 2 and self.__board[i][j + 3] == ' ' and  self.__board[i][j + 4] == 0:
                    self.__board[i][j + 4] = 8
                else:
                    if i > 0 and self.__board[i - 1][j + 2] == ' ' and self.__board[i - 2][j + 2] == 0:
                        self.__board[i - 2][j + 2] = 8
                    if i < self.__size * 2 - 2 and self.__board[i + 1][j + 2] == ' ' and \
                            self.__board[i + 2][j + 2] == 0:
                        self.__board[i + 2][j + 2] = 8

    # fonction qui enlève des "8" du plateau
    def removePossible(self):
        # on parcourt tout le plateau et on remplace les 8 par des 0 dès qu'on en croise un.
        for i in range(0, self.__size * 2 - 1, 2):
            for j in range(0, self.__size * 2 - 1, 2):
                if self.__board[i][j] == 8:
                    self.__board[i][j] = 0

    # fonction qui vérifie si le joueur a gagné.
    def win(self, current_player_id: int) -> bool:
        # Si c'est le joeur 1 qui joue
        if current_player_id == 1:
            # L'opposé de la ligne de départ du joueur 1
            opposite_row = (self.__size * 2) - 2
            # S'il y a un 1 dans la ligne opposée
            if 1 in self.__board[opposite_row]:
                return True

        # Si c'est le joeur 2 qui joue
        elif current_player_id == 2:
            # L'opposé de la ligne de départ du joueur 2
            opposite_row = 0
            # S'il y a un 2 dans la ligne opposée
            if 2 in self.__board[opposite_row]:
                return True

        # Si c'est le joeur 3 qui joue
        elif current_player_id == 3:
            # L'opposé de la colonne de départ du joueur 3
            opposite_col = (self.__size * 2) - 2
            for i in range((self.__size * 2) - 1):
                # S'il y a un 3 dans la colonne opposée
                if self.__board[i][opposite_col] == 3:
                    return True

        # Si c'est le joeur 4 qui joue
        elif current_player_id == 4:
            # L'opposé de la colonne de départ du joueur 4
            opposite_col = 0
            for i in range((self.__size * 2) - 1):
                # S'il y a un 4 dans la colonne opposée
                if self.__board[i][opposite_col] == 4:
                    return True
        return False

    # fonctions de recherche de chemin (celles-ci serve à voir si un chemin existe,
    # pour ce qui est de l'ia et de sa recherche de chemin, le code se trouve dans le module PathFinding (services)
    def pathFindingInit(self, board_init: list, players: Players) -> bool:
        positions = players.getPlayersCoords()
        for i in range(self.__number_of_player + self.__number_of_ai):
            x = positions[i][0]
            y = positions[i][1]
            board = copy.deepcopy(board_init)
            opposite_row = None
            opposite_column = None
            if i == 0:
                opposite_row = (self.__size * 2) - 2
                opposite_column = -1
            elif i == 1:
                opposite_row = 0
                opposite_column = -1
            elif i == 2:
                opposite_row = -1
                opposite_column = (self.__size * 2) - 2
            elif i == 3:
                opposite_row = -1
                opposite_column = 0
            else:
                print('wrong number of player')
            if not self.pathFinding(board, x, y, opposite_row, opposite_column):
                return False
        return True

    def pathFinding(self, board: list, x: int, y: int, opposite_row: int, opposite_column: int) -> bool:
        if x == opposite_row or y == opposite_column:
            # S'il y a un 1 dans la ligne opposée
            return True
        board[x][y] = 9
        if x < self.__size * 2 - 2 and board[x + 1][y] == ' ' and board[x + 2][y] != 9:
            if self.pathFinding(board, x + 2, y, opposite_row, opposite_column):
                return True

        if x > 0 and board[x - 1][y] == ' ' and board[x - 2][y] != 9:
            if self.pathFinding(board, x - 2, y, opposite_row, opposite_column):
                return True

        if y < self.__size * 2 - 2 and board[x][y + 1] == ' ' and board[x][y + 2] != 9:
            if self.pathFinding(board, x, y + 2, opposite_row, opposite_column):
                return True

        if y > 0 and board[x][y - 1] == ' ' and board[x][y - 2] != 9:
            if self.pathFinding(board, x, y - 2, opposite_row, opposite_column):
                return True
        return False

    # Fonction donnant la possibilité à l'utilisateur de mettre une barrière
    def putWall(self, i: int, j: int, board: list, wall_direction: int):
        # on change i et j en focntion de
        i, j = self.changeIAndJ(i, j)
        if wall_direction == 0 and board[i][j - 1] == ' ' and board[i][j] == ' ' and board[i][j + 1] == ' ':
            board[i][j - 1] = 'H'  # barrière à l'horizontale
            board[i][j] = 'I'
            board[i][j + 1] = 'H'
        elif wall_direction == 1 and board[i - 1][j] == ' ' and board[i][j] == ' ' and board[i + 1][j] == ' ':
            board[i + 1][j] = 'V'  # barrière à la verticale
            board[i][j] = 'I'
            board[i - 1][j] = 'V'

    def possibleWall(self, i: int, j: int, board: list, wall_direction: int) -> bool:
        # on change i et j en focntion de
        i, j = self.changeIAndJ(i, j)
        if wall_direction == 0 and board[i][j - 1] == ' ' and board[i][j] == ' ' and board[i][j + 1] == ' ':
            return True
        elif wall_direction == 1 and board[i - 1][j] == ' ' and board[i][j] == ' ' and board[i + 1][j] == ' ':
            return True
        return False

    def changeIAndJ(self, i: int, j: int) -> (int, int):
        if i % 2 == 0:
            if i == self.__size * 2 - 2:
                i -= 1
            else:
                i += 1
        if j % 2 == 0:
            if j == self.__size * 2 - 2:
                j -= 1
            else:
                j += 1
        return i, j

    def setWin(self, win):
        self.__win = win

    def getWin(self):
        return self.__win

