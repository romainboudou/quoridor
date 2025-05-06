# ---------------- imports --------------------

# Entities
from entities.Player import Player

# ValueObjects
from valueobjects.Langues import Langue
from valueobjects.Theme import Theme

# Classe pour la gestion des joueurs
class Players:
    def __init__(self, size: int,
                 number_of_players: int,
                 number_of_ai: int,
                 networking: bool,
                 theme: Theme,
                 langue: Langue):
        self.__size = size
        self.__number_of_players = number_of_players
        self.__number_of_ai = number_of_ai
        self.__networking = networking
        self.__theme = theme
        self.__langue = langue

        # nombres de murs par joueurs
        if self.__size == 5:
            self.__numbers_of_walls = [3, 3, 3, 3]
        elif self.__size == 7:
            self.__numbers_of_walls = [5, 5, 5, 5]
        elif self.__size == 9:
            self.__numbers_of_walls = [7, 7, 7, 7]
        elif self.__size == 11:
            self.__numbers_of_walls = [9, 9, 9, 9]

        #init de players_coords pour la création des players:
        self.__players_coords = [[] for i in range(self.__number_of_players + self.__number_of_ai)]

        self.__players_coords[0] = [0, self.__size - 1]
        self.__players_coords[1] = [self.__size * 2 - 2, self.__size - 1]
        if self.__number_of_players + self.__number_of_ai == 4:
            self.__players_coords[2] = [self.__size - 1, 0]
            self.__players_coords[3] = [self.__size - 1, self.__size * 2 - 2]

        # Création des différents joueur et placement de ceux-ci dans la liste players_list
        self.__players_list = []
        for i in range(self.__number_of_players):
            if i == 0:
                if self.__theme.getName() == "Arcade":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "server",
                                    self.__langue.getText2MenuFin(), "human")
                    self.__players_list.append(player)
                elif self.__theme.getName() == "Classic":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "server",
                                    self.__langue.getText6MenuFin(), "human")
                    self.__players_list.append(player)
            elif i == 1:
                if self.__theme.getName() == "Arcade":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText3MenuFin(), "human")
                    self.__players_list.append(player)
                elif self.__theme.getName() == "Classic":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText7MenuFin(), "human")
                    self.__players_list.append(player)
            elif i == 2:
                if self.__theme.getName() == "Arcade":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText4MenuFin(), "human")
                    self.__players_list.append(player)
                elif self.__theme.getName() == "Classic":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText8MenuFin(), "human")
                    self.__players_list.append(player)
            elif i == 3:
                if self.__theme.getName() == "Arcade":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText5MenuFin(), "human")
                    self.__players_list.append(player)
                elif self.__theme.getName() == "Classic":
                    player = Player(i + 1, self.__players_coords[i], self.__numbers_of_walls[i], "client",
                                    self.__langue.getText9MenuFin(), "human")
                    self.__players_list.append(player)

        for i in range(self.__number_of_ai):
            if self.__theme.getName() == "Arcade":
                player = Player(self.__number_of_players + i + 1, self.__players_coords[number_of_players + i],
                                self.__numbers_of_walls[number_of_players + i], "client", self.__langue.getText3MenuFin(),
                                "ai")
                self.__players_list.append(player)
            elif self.__theme.getName() == "Classic":
                player = Player(self.__number_of_players + i + 1, self.__players_coords[number_of_players + i],
                                self.__numbers_of_walls[number_of_players + i], "client", self.__langue.getText7MenuFin(),
                                "ai")
                self.__players_list.append(player)

        # init du joueur actuel
        self.__current = 0
        self.__current_player = self.__players_list[self.__current]

    # Getters et Setters
    def getCurrentPlayer(self):
        return self.__current_player

    def setCurrentPlayer(self,current):
        while self.__current_player.getId() != current:
            self.changePlayer()
    def getWallNumber(self):
        return self.__current_player.getWallNumber()

    def removeWallFromPlayer(self):
        self.__current_player.setWallNumber(self.__current_player.getWallNumber() - 1)

    def getPlayersCoords(self):
        players_coords = []
        for i in range(self.__number_of_players + self.__number_of_ai):
            players_coords.append(self.__players_list[i].getPlayerCoords())
        return players_coords

    def setPlayersCoords(self, list: list):
        for index, player in enumerate(self.__players_list):
            player.setPlayerCoords(list[index])

    def getplayerliste(self):
        return self.__players_list

    # fonction qui change le joueur actuel et change la position du joueur actuel
    def changePlayer(self):
        if self.__current == self.__number_of_players + self.__number_of_ai - 1:
            self.__current = 0
            self.__current_player = self.__players_list[self.__current]
        else:
            self.__current += 1
            self.__current_player = self.__players_list[self.__current]

