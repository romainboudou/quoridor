# ---------------- imports --------------------
import pygame
import pickle
import os

# Entities
from entities.Players import Players

# ValueObjects
from valueobjects.Board import Board

# L'utilisation de pickle à été gardé car ce module de python permet de sauvegarder/charger
# des données dans des fichiers pkl et de garder simplement la structure de ces données

# classe qui va gérer la sauvegarde et le chargement de partie
class PickleHandler:
    def __init__(self, name: str):
        self.__name = f"saves/{name}.pkl"

    # fonction qui gère la sauvegarde
    def save(self, board: Board, players: Players, time: int):
        if not os.path.exists("saves"):
            os.makedirs("saves")
        try:
            # on essaie d'ouvrir le fichier, si il n'existe pas on le créé (ab)
            file = open(self.__name, "ab")
            file.close()

            # puis on ajoute à l'intérieur le l'objet board, l'object players, et le temps de jeu
            with open(self.__name, "wb") as output_file:
                pickle.dump(board, output_file, pickle.HIGHEST_PROTOCOL)
                pickle.dump(players, output_file, pickle.HIGHEST_PROTOCOL)
                pickle.dump(time, output_file, pickle.HIGHEST_PROTOCOL)

            output_file.close()
            return True
        # sinon on retourne une erreur
        except Exception as e:
            return False

    # fonction qui va charger la partie depuis un fichier existant

    def load(self) -> (str, Board, Players, int):
        try:
            with open(self.__name, "rb") as input_file:
                board = pickle.load(input_file)
                players = pickle.load(input_file)
                time = pickle.load(input_file)

            input_file.close()
            return "", board, players, time
        except Exception as e:
            return "error", None, None, 0
