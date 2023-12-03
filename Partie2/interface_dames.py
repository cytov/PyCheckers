# Auteurs: À compléter

from tkinter import Tk, Label, NSEW, Button
from Partie2.canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position
from Partie1.damier import Damier


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        msg_couleur (Label): Affiche la couleur du joueur qui doit faire un déplacement
        msg_deplacement (Label): Affiche si le jeton sélectionné peut se déplacer
        bouton_quitter (Button): Bouton permettant de quitter la partie
        TODO: AJOUTER VOS PROPRES ATTRIBUTS ICI!
    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Affiche si la pièce sélectionnée peut se déplacer
        self.msg_deplacement = Label(self)
        self.msg_deplacement.grid

        # Affiche le nom du joueur qui joue actuellement
        self.msg_couleur = Label(self)
        self.msg_couleur.grid()

        # Appel initial pour afficher la couleur du joueur
        self.joueur_en_cours()

        # Affiche un bouton pour quitter la partie
        self.bouton_quitter = Button(self, text="Quitter la partie", command=self.quitter_la_partie)
        self.bouton_quitter.grid(row=0, column=1, sticky='ne')

        # Affiche un bouton pour lancer une nouvelle partie
        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.grid(row=0, column=2, sticky='ne')

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        if event is not None:

            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne = event.y // self.canvas_damier.n_pixels_par_case
            colonne = event.x // self.canvas_damier.n_pixels_par_case
            position = Position(ligne, colonne)

            # On récupère l'information sur la pièce à l'endroit choisi.
            piece = self.partie.damier.recuperer_piece_a_position(position)

            if piece is None:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
            else:
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format( position)
        #         self.piece_peut_etre_deplacee()
        #
        #         if position is not None:
        #             self.piece_peut_etre_deplacee()
        #
        #         return position
        #
        # return None

    # def piece_peut_etre_deplacee(self):
    #
    #     """ Méthode permettant de savoir si la piece sélectionnée peut être déplacée
    #
    #     Args :
    #
    #     """
    #     position_piece = self.selectionner(None)
    #     deplacement = self.partie.damier.piece_peut_se_deplacer(position_piece)
    #
    #     if deplacement:
    #         self.msg_deplacement['foreground'] = 'black'
    #         self.msg_deplacement['text'] = 'La pièce peut se déplacer'
    #     else:
    #         self.msg_deplacement['foreground'] = 'red'
    #         self.msg_deplacement['text'] = 'La pièce ne peut pas se déplacer'

    def nouvelle_partie(self):
        """ Méthode pour lancer une nouvelle partie. """

        self.partie = Partie()
        self.messages['text'] = "Nouvelle partie commencée."
        self.joueur_en_cours()

    def quitter_la_partie(self):
        """ Méthode de quitter la fenêtre de la partie."""
        self.quit()

    def joueur_en_cours(self):
        """ Méthode permettant de savoir quel joueur a son tour actif et l'afficher sous forme de message

        """

        couleur = self.partie.couleur_joueur_courant
        self.msg_couleur['foreground'] = 'black'
        self.msg_couleur['text'] = "C'est le tour du joueur {}".format(couleur)

        # TODO: À continuer....


