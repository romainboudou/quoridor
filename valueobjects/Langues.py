# -------------- CLASSE QUI LA LANGUE --------------#
class Langue:
    def __init__(self, name: str):
        self.__name = name

        if self.__name == "french":
            # Menu principal
            self.__text1_menu_principale = "Nouvelle partie"
            self.__text2_menu_principale = "Charger une partie"
            self.__text3_menu_principale = "Parametres"

            # Menu Settings
            self.__text1_menu_settings = "Parametres"
            self.__text2_menu_settings = "Langues"
            self.__text3_menu_settings = "Themes"
            self.__text4_menu_settings = "Classique"
            self.__text5_menu_settings = "Arcade"
            self.__text7_menu_settings = "Anglais"
            self.__text8_menu_settings = "Francais"
            self.__text9_menu_settings = "Valider"
            self.__text10_menu_settings = "Volume :"
            self.__text11_menu_settings = "Muet"

            # Menu Game Mode
            self.__text1_game_mode = "Mode de jeu"
            self.__text2_game_mode = "Local"
            self.__text3_game_mode = "En ligne"

            # Menu New Game
            self.__text1_new_game = "Plateau"
            self.__text2_new_game = "Joueurs"
            self.__text3_new_game = "IA"
            self.__text4_new_game = "Jouer !"

            # Menu Client Serveur
            self.__text1_client_serveur = "Creation serveur"
            self.__text2_client_serveur = "Creer une partie"
            self.__text3_client_serveur = "Deja une invitation ?"
            self.__text4_client_serveur = "Entrez l'adresse IP..."
            self.__text5_client_serveur = "Mauvaise adresse IP"

            # Menu Load Game
            self.__text1_load_game = "Charger une partie"
            self.__text2_load_game = "Deja une sauvegarde ?"
            self.__text3_load_game = "Nom du fichier..."
            self.__text4_load_game = "fichier introuvable"

            # Menu Settings Game
            self.__text1_settings_game = "Parametres"
            self.__text2_settings_game = "Sauvegarder"
            self.__text3_settings_game = "Recommencer"
            self.__text4_settings_game = "Quitter"
            self.__text5_settings_game = "Reussi"
            self.__text6_settings_game = "erreur"
            self.__text7_settings_game = "Valider"

            # Waiting
            self.__text1_waiting = "En attente de tout les joueurs..."
            self.__text2_waiting = "Votre adresse IP:"

            # Game
            self.__text1_game = 'murs:'
            self.__text2_game = 'Actuel'

            # Menu Fin
            self.__text1_fin = " gagne !"
            self.__text2_fin = "ETOILE"
            self.__text3_fin = "COEUR"
            self.__text4_fin = "TREFLE"
            self.__text5_fin = "NOTE DE MUSIQUE"
            self.__text6_fin = "FLEUR"
            self.__text7_fin = "CHAMPIGNON"
            self.__text8_fin = "PAPILLON"
            self.__text9_fin = "FEUILLE"

        elif self.__name == "english":
            # Menu principal
            self.__text1_menu_principale = "New Game"
            self.__text2_menu_principale = "Load Game"
            self.__text3_menu_principale = "Settings"

            # Menu Settings
            self.__text1_menu_settings = "Settings"
            self.__text2_menu_settings = "Languages"
            self.__text3_menu_settings = "Themes"
            self.__text4_menu_settings = "Classic"
            self.__text5_menu_settings = "Arcade"
            self.__text7_menu_settings = "English"
            self.__text8_menu_settings = "French"
            self.__text9_menu_settings = "Validate"
            self.__text10_menu_settings = "Volume :"
            self.__text11_menu_settings = "Mute"

            # Menu Game Mode
            self.__text1_game_mode = "Game mode"
            self.__text2_game_mode = "Solo"
            self.__text3_game_mode = "Multiplayer"

            # Menu New Game
            self.__text1_new_game = "Board"
            self.__text2_new_game = "Players"
            self.__text3_new_game = "AI"
            self.__text4_new_game = "Start!"

            # Menu Client Serveur
            self.__text1_client_serveur = "Creation server"
            self.__text2_client_serveur = "Create a game"
            self.__text3_client_serveur = "Already an invitation?"
            self.__text4_client_serveur = "Enter the IP address..."
            self.__text5_client_serveur = "Wrong IP address"

            # Menu Load Game
            self.__text1_load_game = "Load Game"
            self.__text2_load_game = "Already have a backup?"
            self.__text3_load_game = "File name..."
            self.__text4_load_game = "unknown file"

            # Menu Settings Game
            self.__text1_settings_game = "Settings"
            self.__text2_settings_game = "Save"
            self.__text3_settings_game = "Restart"
            self.__text4_settings_game = "Quit"
            self.__text5_settings_game = "done"
            self.__text6_settings_game = "error"
            self.__text7_settings_game = "Validate"

            # Waiting
            self.__text1_waiting = "Waiting for everyone to connect..."
            self.__text2_waiting = "Your ip adress:"

            # Game
            self.__text1_game = 'walls:'
            self.__text2_game = 'Current'

            # Menu Fin
            self.__text1_fin = " win!"
            self.__text2_fin = "STAR"
            self.__text3_fin = "HEART"
            self.__text4_fin = "CLOVER"
            self.__text5_fin = "MUSIC NOTE"
            self.__text6_fin = "FLOWER"
            self.__text7_fin = "MUSHROOM"
            self.__text8_fin = "BUTTERFLY"
            self.__text9_fin = "LEAF"

# -------------- GETTERS --------------#
    # -------------- Getter NAME --------------#
    def getName(self) -> str:
        return self.__name

    # -------------- Getter-Menu Principale --------------#
    def getText1MenuPrincipale(self) -> str:
        return self.__text1_menu_principale

    def getText2MenuPrincipale(self) -> str:
        return self.__text2_menu_principale

    def getText3MenuPrincipale(self) -> str:
        return self.__text3_menu_principale

    # -------------- Getter-Menu Settings --------------#
    def getText1MenuSettings(self) -> str:
        return self.__text1_menu_settings

    def getText2MenuSettings(self) -> str:
        return self.__text2_menu_settings

    def getText3MenuSettings(self) -> str:
        return self.__text3_menu_settings

    def getText4MenuSettings(self) -> str:
        return self.__text4_menu_settings

    def getText5MenuSettings(self) -> str:
        return self.__text5_menu_settings

    def getText7MenuSettings(self) -> str:
        return self.__text7_menu_settings

    def getText8MenuSettings(self) -> str:
        return self.__text8_menu_settings

    def getText9MenuSettings(self) -> str:
        return self.__text9_menu_settings

    def getText10MenuSettings(self) -> str:
        return self.__text10_menu_settings

    def getText11MenuSettings(self) -> str:
        return self.__text11_menu_settings

    # -------------- Getter-Menu Mode --------------#
    def getText1MenuMode(self) -> str:
        return self.__text1_game_mode

    def getText2MenuMode(self) -> str:
        return self.__text2_game_mode

    def getText3MenuMode(self) -> str:
        return self.__text3_game_mode

# -------------- Getter-Menu New Game --------------#
    def getText1MenuNewGame(self) -> str:
        return self.__text1_new_game

    def getText2MenuNewGame(self) -> str:
        return self.__text2_new_game

    def getText3MenuNewGame(self) -> str:
        return self.__text3_new_game

    def getText4MenuNewGame(self) -> str:
        return self.__text4_new_game

# -------------- Getter-Menu Client Serveur --------------#

    def getText1MenuClientServeur(self) -> str:
        return self.__text1_client_serveur

    def getText2MenuClientServeur(self) -> str:
        return self.__text2_client_serveur

    def getText3MenuClientServeur(self) -> str:
        return self.__text3_client_serveur

    def getText4MenuClientServeur(self) -> str:
        return self.__text4_client_serveur

    def getText5MenuClientServeur(self) -> str:
        return self.__text5_client_serveur

# -------------- Getter-Menu Load Game --------------#

    def getText1MenuLoadGame(self) -> str:
        return self.__text1_load_game

    def getText2MenuLoadGame(self) -> str:
        return self.__text2_load_game

    def getText3MenuLoadGame(self) -> str:
        return self.__text3_load_game

    def getText4MenuLoadGame(self) -> str:
        return self.__text4_load_game

    # -------------- Getter-Menu Settings Game --------------#

    def getText1MenuSettingsGame(self) -> str:
        return self.__text1_settings_game

    def getText2MenuSettingsGame(self) -> str:
        return self.__text2_settings_game

    def getText3MenuSettingsGame(self) -> str:
        return self.__text3_settings_game

    def getText4MenuSettingsGame(self) -> str:
        return self.__text4_settings_game

    def getText5MenuSettingsGame(self) -> str:
        return self.__text5_settings_game

    def getText6MenuSettingsGame(self) -> str:
        return self.__text6_settings_game

    def getText7MenuSettingsGame(self) -> str:
        return self.__text7_settings_game

    # -------------- Getter-Waiting --------------#
    def getText1Waiting(self):
        return self.__text1_waiting

    def getText2Waiting(self):
        return self.__text2_waiting

    # -------------- Getter-Game --------------#

    def getText1Game(self) -> str:
        return self.__text1_game

    def getText2Game(self) -> str:
        return self.__text2_game

    # -------------- Getter-Menu Fin --------------#

    def getText1MenuFin(self) -> str:
        return self.__text1_fin

    def getText2MenuFin(self) -> str:
        return self.__text2_fin

    def getText3MenuFin(self) -> str:
        return self.__text3_fin

    def getText4MenuFin(self) -> str:
        return self.__text4_fin

    def getText5MenuFin(self) -> str:
        return self.__text5_fin

    def getText6MenuFin(self) -> str:
        return self.__text6_fin

    def getText7MenuFin(self) -> str:
        return self.__text7_fin

    def getText8MenuFin(self) -> str:
        return self.__text8_fin

    def getText9MenuFin(self) -> str:
        return self.__text9_fin
