# La classe pour le pathfinding de l'ia qui représente les cases où les joueurs peuvent se déplacer
class Node:
    def __init__(self, x: int, y: int, parent = None):
        self.__position = (x, y)
        self.__h = 0
        self.__g = 0
        self.__f = 0
        self.__parent = parent

    # Surcharge de l'égalité pour comparer la position de deux nodes
    def __eq__(self, other):
        return self.getPosition() == other.getPosition()

    # Getters et Setters
    def getPosition(self):
        return self.__position
    def getF(self):
        return self.__f

    def setF(self, f):
        self.__f = f

    def getG(self):
        return self.__g

    def setG(self, g):
        self.__g = g

    def getH(self):
        return self.__h

    def setH(self, h):
        self.__h = h

    def getParent(self):
        return self.__parent

    def setParent(self, parent):
        self.__parent = parent

