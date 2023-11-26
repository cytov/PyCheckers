# Auteurs: À compléter


class Position:
    """Une position à deux coordonnées: ligne et colonne. La convention utilisée est celle de la notation matricielle :
    le coin supérieur gauche d'une matrice est dénoté (0, 0) (ligne 0 et colonne 0). On additionne une unité de colonne
    lorsqu'on se déplace vers la droite, et une unité de ligne lorsqu'on se déplace vers le bas.

    +-------+-------+-------+-------+
    | (0,0) | (0,1) | (0,2) |  ...  |
    | (1,0) | (1,1) | (1,2) |  ...  |
    | (2,0) | (2,1) | (2,2) |  ...  |
    |  ...  |  ...  |  ...  |  ...  |
    +-------+-------+-------+-------+

    Attributes:
        ligne (int): La ligne associée à la position.
        colonne (int): La colonne associée à la position

    """
    def __init__(self, ligne, colonne):
        """Constructeur de la classe Position. Initialise les deux attributs de la classe.

        Args:
            ligne (int): La ligne à considérer dans l'instance de Position.
            colonne (int): La colonne à considérer dans l'instance de Position.

        """
        self.ligne = int(ligne)
        self.colonne = int(colonne)

    def positions_diagonales_bas(self):
        """Retourne une liste contenant les deux positions diagonales bas à partir de la position actuelle.

        Note:
            Dans cette méthode et les prochaines, vous n'avez pas à valider qu'une position est "valide", car dans le
            contexte de cette classe toutes les positions (même négatives) sont permises.

        Returns:
            list: La liste des deux positions.

        """
        return [Position(self.ligne + 1, self.colonne - 1), Position(self.ligne + 1, self.colonne + 1)]

    def positions_diagonales_haut(self):
        """Retourne une liste contenant les deux positions diagonales haut à partir de la position actuelle.

        Returns:
            list: La liste des deux positions.

        """
        return [Position(self.ligne - 1, self.colonne - 1), Position(self.ligne - 1, self.colonne + 1)]

    def quatre_positions_diagonales(self):
        """Retourne une liste contenant les quatre positions diagonales à partir de la position actuelle.

        Returns:
            list: La liste des quatre positions.

        """
        return self.positions_diagonales_bas() + self.positions_diagonales_haut()

    def quatre_positions_sauts(self):
        """Retourne une liste contenant les quatre "sauts" diagonaux à partir de la position actuelle. Les positions
        retournées sont donc en diagonale avec la position actuelle, mais a une distance de 2.

        Returns:
            list: La liste des quatre positions.

        """
        positions_intermediaires = self.quatre_positions_diagonales()

        return [positions_intermediaires[n].quatre_positions_diagonales()[n] for n in range(4)]

    def trouver_position_milieu_saut(self, position_piece, position_cible):
        """Cette méthode détermine la position diagonale entre une position de depart, et une position cible de saut

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            Position: La position au milieu du saut.

        """
        return self.__init__((position_piece.ligne + position_cible.ligne) // 2, (position_piece.colonne + position_cible.colonne) // 2)

    def __eq__(self, other):
        """Méthode spéciale indiquant à Python comment vérifier si deux positions sont égales. On compare simplement
        la ligne et la colonne de l'objet actuel et de l'autre objet.

        """
        return self.ligne == other.ligne and self.colonne == other.colonne

    def __repr__(self):
        """Méthode spéciale indiquant à Python comment représenter une instance de Position par une chaîne de
        caractères. Notamment utilisé pour imprimer une position à l'écran.

        """
        return '({}, {})'.format(self.ligne, self.colonne)

    def __hash__(self):
        """Méthode spéciale indiquant à Python comment "hasher" une Position. Cette méthode est nécessaire si on veut
        utiliser une classe que nous avons définie nous mêmes comme clé d'un dictionnaire.
        Les étudiants(es) curieux(ses) peuvent consulter wikipédia pour en savoir plus:
            https://fr.wikipedia.org/wiki/Fonction_de_hachage

        """
        return hash(str(self))


if __name__ == '__main__':
    print('Test unitaires de la classe "Position"...')

    pos = Position(3, 4)
    assert pos.ligne == 3
    assert pos.colonne == 4

    assert pos.positions_diagonales_bas() == [Position(4, 3), Position(4, 5)]
    assert pos.positions_diagonales_haut() == [Position(2, 3), Position(2, 5)]
    assert pos.quatre_positions_diagonales() == [Position(4, 3), Position(4, 5), Position(2, 3), Position(2, 5)]
    assert pos.quatre_positions_sauts() == [Position(5, 2), Position(5, 6), Position(1, 2), Position(1, 6)]

    print('Test unitaires passés avec succès!')
