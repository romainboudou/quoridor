# Classe pour la gestion d'un joueur en particulier
class Player:
    def __init__(self, id: int, player_coords: list, wall_number: int, networking: str, name: str, type_of_player: str = "human"):
        self.__id = id
        self.__type_of_player = type_of_player
        self.__player_coords = player_coords
        self.__networking = networking
        self.__name = name
        self.__wall_number = wall_number

    # Getters et Setters
    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getTypeOfPlayer(self):
        return self.__type_of_player

    def getWallNumber(self):
        return self.__wall_number

    def setWallNumber(self, nb):
        self.__wall_number = nb
    def getPlayerCoords(self):
        return self.__player_coords

    def setPlayerCoords(self, coords: list):
        self.__player_coords = coords


