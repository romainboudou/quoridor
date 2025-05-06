# ---------------- imports --------------------
# valueobjects
from valueobjects.Board import Board

# entities
from entities.Node import Node


# -------------- CLASSE DE RECHERCHE DE CHEMIN POUR L'IA  --------------#
class PathFinding:
    def __init__(self, board: list, size):
        self.__closed_list = []
        self.__open_list = []
        self.__board = board
        self.__size = size
        self.__path = []

    def pathFinding(self, start: list, target: list):
        self.__path = []
        self.__closed_list = []
        self.__open_list = []
        board = self.__board
        size = self.__size
        total_size = size * 2 - 1

        starting_node = Node(start[0], start[1])
        end_node = Node(target[0], target[1])
        self.__open_list.append(starting_node)

        iteration = 0
        max_iterations = total_size * total_size // 2
        # on loop tant que la liste des nodes ouvertes n'est pas vide
        while len(self.__open_list) > 0:
            # check si le joueur adverse est sur la case target (cas de boucle infini)
            if board[target[0]][target[1]] != 0:
                return None

            # nb maximum de loop:
            iteration += 1
            if iteration > max_iterations:
                # too long, no path or blocked by wall
                return None

            current_node = self.__open_list[0]
            current_index = 0

            # la current node est la node avec la valeur de f la plus basse
            for index, node in enumerate(self.__open_list):
                if node.getF() < current_node.getF():
                    current_node = node
                    current_index = index

            # on l'enleve de current, et on l'ajoute a closed
            self.__open_list.pop(current_index)
            self.__closed_list.append(current_node)

            # target trouvé:
            if current_node == end_node:
                current = current_node
                while current is not None:
                    self.__path.append(current.getPosition())
                    current = current.getParent()

                return self.__path[::-1]

            # GENERATION DES ENFANTS:
            children = []
            # génération des enfants directement adjacent:
            for index, new_pos in enumerate([(0, 2), (0, -2), (-2, 0), (2, 0)]):
                # position de l'enfant
                x = current_node.getPosition()[0] + new_pos[0]
                y = current_node.getPosition()[1] + new_pos[1]

                # check si enfant dans le plateau de jeu
                if x > total_size or x < 0 or y > total_size or y < 0:
                    continue

                # si la case contient un joueur impossible de s'y deplacer
                # (reciproquement, si la case ne contient pas un joueur, le mouvement est possible):
                if board[x][y] != 0 and board[x][y] != 2:
                    continue

                # check si l'enfant à passé un mur:
                if index == 0:
                    if board[x][y - 1] == 'V':
                        continue
                elif index == 1:
                    if board[x][y + 1] == 'V':
                        continue
                elif index == 2:
                    if board[x + 1][y] == 'H':
                        continue
                elif index == 3:
                    if board[x - 1][y] == 'H':
                        continue

                new_node = Node(x, y, parent=current_node)
                children.append(new_node)

            # génération des enfants qui ont sauté un joueur:
            for index, new_pos in enumerate([(0, 4), (0, -4), (-4, 0), (4, 0)]):
                # position de l'enfant
                x = current_node.getPosition()[0] + new_pos[0]
                y = current_node.getPosition()[1] + new_pos[1]

                # check si enfant dans le plateau de jeu
                if x > total_size or x < 0 or y > total_size or y < 0:
                    continue

                # si la case contient un joueur impossible de s'y deplacer
                # (reciproquement, si la case ne contient pas un joueur, le mouvement est possible):
                if board[x][y] != 0 and board[x][y] != 2:
                    continue

                # check si l'enfant à passé un mur (alors on stoppe)
                # et que l'enfant est bien passé au dessus d'un joueur:

                if index == 0:
                    if board[x][y - 1] == 'V' or board[x][y - 2] == 0 or board[x][y - 3] == 'V':
                        continue
                elif index == 1:
                    if board[x][y + 1] == 'V' or board[x][y + 2] == 0 or board[x][y + 3] == 'V':
                        continue
                elif index == 2:
                    if board[x + 1][y] == 'H' or board[x + 2][y] == 0 or board[x + 3][y] == 'H':
                        continue
                elif index == 3:
                    if board[x - 1][y] == 'H' or board[x - 2][y] == 0 or board[x - 3][y] == 'H':
                        continue

                new_node = Node(x, y, parent=current_node)
                children.append(new_node)

            # génération des enfants qui ont bougé en diagonal grace a un joueur et un mur:
            for index, new_pos in enumerate([(2, 2), (2, -2), (-2, 2), (-2, -2)]):
                # position de l'enfant
                x = current_node.getPosition()[0] + new_pos[0]
                y = current_node.getPosition()[1] + new_pos[1]

                # check si enfant dans le plateau de jeu
                if x > total_size or x < 0 or y > total_size or y < 0:
                    continue

                # si la case contient un joueur impossible de s'y deplacer
                # (reciproquement, si la case ne contient pas un joueur, le mouvement est possible):
                if board[x][y] != 0 and board[x][y] != 2:
                    continue

                a = b = c = d = e = f = g = h = i = j = k = l = m = n = o = p = True
                # cas des diagonales (on vérifie si on est bien dans le cas d'un mouvement diagonal comme expliqué
                # dans les regles du jeu
                if index == 0:
                    if total_size > x + 1 and x - 1 >= 0 and y - 2 >= 0:
                        if board[x - 1][y - 2] == ' ' and board[x][y - 2] == 1 and board[x + 1][y - 2] == 'H' and \
                                board[x][y - 1] == ' ':
                            a = False
                    elif x - 2 >= 0 and y - 1 >= 0 and y + 1 < total_size:
                        if board[x - 2][y - 1] == ' ' and board[x - 2][y] == 1 and board[x - 2][y + 1] == 'V' and \
                                board[x - 1][y] == ' ':
                            b = False

                elif index == 1:
                    if total_size > x + 1 and x - 1 >= 0 and y + 2 < total_size:
                        if board[x - 1][y + 2] == ' ' and board[x][y + 2] == 1 and board[x + 1][y + 2] == 'H' and \
                                board[x][y + 1] == ' ':
                            c = False
                    if x - 2 > 0 and y - 1 >= 0 and y + 1 < total_size:
                        if board[x - 2][y + 1] == ' ' and board[x - 2][y] == 1 and board[x - 2][y - 1] == 'V' and \
                                board[x - 1][y] == ' ':
                            d = False

                elif index == 2:
                    if total_size > x + 2 and y - 1 >= 0 and y + 1 < total_size:
                        if board[x + 2][y - 1] == ' ' and board[x + 2][y] == 1 and board[x + 2][y + 1] == 'V' and \
                                board[x + 1][y] == ' ':
                            e = False
                    if total_size > x + 1 and x - 1 >= 0 and y - 2 > 0:
                        if board[x + 1][y - 2] == ' ' and board[x][y - 2] == 1 and board[x - 1][y - 2] == 'H' and \
                                board[x][y - 1] == ' ':
                            f = False

                elif index == 3:
                    if total_size > x + 2 and y - 1 >= 0 and y + 1 < total_size:
                        if board[x + 2][y + 1] == ' ' and board[x + 2][y] == 1 and board[x + 2][y - 1] == 'V' and \
                                board[x + 1][y] == ' ':
                            g = False
                    if total_size > x + 1 and x - 1 >= 0 and y + 2 < total_size:
                        if board[x + 1][y + 2] == ' ' and board[x][y + 2] == 1 and board[x - 1][y + 2] == 'H' and \
                                board[x][y + 1] == ' ':
                            h = False
                # cas ou ce n'est pas un mur mais le bord du terrain apres le joueur adverse
                if index == 0:
                    if x - 1 >= 0 and y - 2 >= 0:
                        if board[x - 1][y - 2] == ' ' and board[x][y - 2] == 1 and x + 1 > total_size \
                                and board[x][y - 1] == ' ':
                            i = False
                    elif x - 2 >= 0 and y - 1 >= 0:
                        if board[x - 2][y - 1] == ' ' and board[x - 2][y] == 1 and y + 1 > total_size \
                                and board[x - 1][y] == ' ':
                            j = False

                elif index == 1:
                    if x - 1 >= 0 and y + 2 < total_size:
                        if board[x - 1][y + 2] == ' ' and board[x][y + 2] == 1 and x + 1 > total_size \
                                and board[x][y + 1] == ' ':
                            k = False
                    if x - 2 > 0 and y - 2 >= 0 and y + 1 < total_size:
                        if board[x - 2][y + 1] == ' ' and board[x - 2][y] == 1 and y - 1 < 0 and board[x - 1][y] == ' ':
                            l = False

                elif index == 2:
                    if total_size > x + 2 and y - 1 >= 0:
                        if board[x + 2][y - 1] == ' ' and board[x + 2][y] == 1 and y + 1 > total_size \
                                and board[x + 1][y] == ' ':
                            m = False
                    if total_size > x + 1 and y - 2 > 0:
                        if board[x + 1][y - 2] == ' ' and board[x][y - 2] == 1 and x - 1 < 0 and board[x][y - 1] == ' ':
                            n = False

                elif index == 3:
                    if total_size > x + 2 and y + 1 < total_size:
                        if board[x + 2][y + 1] == ' ' and board[x + 2][y] == 1 and y - 1 < 0 and board[x + 1][y] == ' ':
                            o = False
                    if total_size > x + 1 and y + 2 < total_size:
                        if board[x + 1][y + 2] == ' ' and board[x][y + 2] == 1 and x - 1 < 0 and board[x][y + 1] == ' ':
                            p = False
                # si un mouvement diagonal parmis les quatres possible est vrai
                # alors on ajoute l'enfant à la liste open_list
                if index == 0:
                    if a and b and i and j:
                        continue
                elif index == 1:
                    if c and d and k and l:
                        continue
                elif index == 2:
                    if e and f and m and n:
                        continue
                elif index == 3:
                    if g and h and o and p:
                        continue

                new_node = Node(x, y, parent=current_node)
                children.append(new_node)

            # Tout les enfants ont maintenant été rajouté !

            # on boucle sur les enfants
            for child in children:

                # f, g et h value:
                child.setG(((child.getPosition()[0] - current_node.getPosition()[0]) ** 2) + (
                        (child.getPosition()[1] - current_node.getPosition()[1]) ** 2))
                child.setH(((child.getPosition()[0] - end_node.getPosition()[0]) ** 2) + (
                        (child.getPosition()[1] - end_node.getPosition()[1]) ** 2))
                child.setF(child.getG() + child.getH())

                can_append = True

                # l'enfant fait il partie de closed_list et sa valeur de F est elle plus plus grande ?
                # si oui, ne pas la rajouter à open_list
                for closed_child in self.__closed_list:
                    if child == closed_child and child.getF() >= closed_child.getF():
                        can_append = False

                # l'enfant fait il partie de open_list et sa valeur de F est elle plus plus grande ?
                # si oui, ne pas la rajouter à open_list
                for open_node in self.__open_list:
                    if child == open_node and child.getF() >= open_node.getF():
                        can_append = False

                # si elle n'était pas dans open ou closed list alors on peut l'ajouter à open_list
                # cf l'utiliser pour la prochaine itération
                if can_append:
                    self.__open_list.append(child)

        return None
