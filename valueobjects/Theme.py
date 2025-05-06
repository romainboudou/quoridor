# -------------- CLASSE QUI GERE LE THEME --------------#
class Theme:
    def __init__(self, name: str, colorP: tuple, colorS: tuple, sizeFontTitle: int, sizeFontButton: int, font1: str,
                 font2: str, imagebg: str, imagebg2: str, tooltipFR: str, tooltipENG: str, image_player1: str, image_player2: str, image_player3: str,
                 image_player4: str, color_case: tuple, color_board: tuple, color_choice: tuple, color_wall: tuple,
                 audio: str):
        self.__name = name
        self.__colorP = colorP
        self.__colorS = colorS
        self.__size_font_title = sizeFontTitle
        self.__size_font_button = sizeFontButton
        self.__font1 = font1
        self.__font2 = font2
        self.__imagebg = imagebg
        self.__imagebg2 = imagebg2
        self.__tooltip_FR = tooltipFR
        self.__tooltip_ENG = tooltipENG
        self.__image_player1 = image_player1
        self.__image_player2 = image_player2
        self.__image_player3 = image_player3
        self.__image_player4 = image_player4
        self.__color_case = color_case
        self.__color_board = color_board
        self.__color_choice = color_choice
        self.__color_wall = color_wall
        self.__audio = audio

# GETTERS ET SETTERS
    def getName(self) -> str:
        return self.__name

    def getColorP(self):
        return self.__colorP

    def getColorS(self):
        return self.__colorS

    def getSizeFontTitle(self):
        return self.__size_font_title

    def getSizeFontButton(self):
        return self.__size_font_button

    def getFont1(self):
        return self.__font1

    def getFont2(self):
        return self.__font2

    def getImagebg(self) -> str:
        return self.__imagebg

    def getImagebg2(self) -> str:
        return self.__imagebg2

    def getTooltipFR(self) -> str:
        return self.__tooltip_FR

    def getTooltipENG(self) -> str:
        return self.__tooltip_ENG
    def getImagePlayer1(self) -> str:
        return self.__image_player1

    def getImagePlayer2(self) -> str:
        return self.__image_player2

    def getImagePlayer3(self) -> str:
        return self.__image_player3

    def getImagePlayer4(self) -> str:
        return self.__image_player4

    def getColorCase(self):
        return self.__color_case

    def getColorBoard(self):
        return self.__color_board

    def getColorChoice(self):
        return self.__color_choice

    def getColorWall(self):
        return self.__color_wall

    def getAudio(self) -> str:
        return self.__audio

    def setSizeFontButton(self, nb):
        self.__size_font_button = nb

    def setSizeFontTitle(self, nb):
        self.__size_font_title = nb