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
        msg_pos_source (Label): Affiche valeur de pos_source_selectionnee
        msg_pos_cible (Label): Affiche valeur de pos_cible_selectionnee
        bouton_quitter (Button): Bouton permettant de quitter la partie
        bouton_nouvelle_partie (Button) : Bouton permettant de faire une nouvelle partie
        pos_source_selectionnee (Position) : Position de depart selectionnee
        damier (Damier) : Le damier du jeu
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

        # Affiche le nom du joueur qui joue actuellement
        self.msg_couleur = Label(self)
        self.msg_couleur.grid()

        # Appel initial pour afficher la couleur du joueur
        self.joueur_en_cours()

        # Appel initial pour savoir si la pièce doit prendre doit prendre
        self.partie.doit_prendre = False

        # Affiche un bouton pour quitter la partie
        self.bouton_quitter = Button(self, text="Quitter la partie", command=self.quitter_la_partie)
        self.bouton_quitter.grid(row=0, column=1, sticky='ne')

        # Affiche un bouton pour lancer une nouvelle partie
        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.grid(row=0, column=2, sticky='ne')

        # Ajout d'une variable de classe pour stocker la position source
        self.pos_source_selectionnee = None

        # Ajout d'une variable de classe pour stocker la position cible
        self.pos_cible_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Message pour voir la trace de la position source
        self.msg_pos_source = Label(self)
        self.msg_pos_source.grid()

        # Message pour voir la trace de la position cible
        self.msg_pos_cible = Label(self)
        self.msg_pos_cible.grid()

        # Lancement des positions
        self.trace()

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        Returns:
            pos_source_selectionnee (int) : La position de la piece que l'on veut deplacer
            pos_cible_selectionne (int) : La position vers laquelle on veut envoyer notre piece

        """

        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)

        if self.pos_source_selectionnee is None:
            if piece is None:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
            elif piece.couleur != self.partie.couleur_joueur_courant:
                self.messages['foreground'] = 'red'
                self.messages['text'] = "Veuillez sélectionner une pièce de la bonne couleur."
            else:
                self.pos_source_selectionnee = position
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)
                self.trace()
        else:
            if piece is not None and piece.couleur == self.partie.couleur_joueur_courant:
                self.pos_source_selectionnee = position
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Position source sélectionnée à {}.'.format(position)
            else:
                if (self.pos_source_selectionnee is not None
                        and position in self.pos_source_selectionnee.quatre_positions_diagonales()
                        and self.partie.damier.piece_peut_se_deplacer_vers(self.pos_source_selectionnee, position)):
                    self.pos_cible_selectionnee = position
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Position cible sélectionnée à {}.'.format(position)
                    self.effectuer_deplacement(self.pos_source_selectionnee, self.pos_cible_selectionnee)
                else:
                    self.messages['foreground'] = 'red'
                    self.messages['text'] = "Position cible non valide"

        return self.pos_source_selectionnee, self.pos_cible_selectionnee


    def effectuer_deplacement(self, pos_source, pos_cible):
        """Méthode permettant de déplacer un jeton suite aux clics.

        Args:
            pos_source (position): La position de la pièce que l'on veut déplacer
            pos_cible (position): La position vers laquelle on veut envoyer la pièce soit par déplacement soit en mangeant une autre pièce.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        self.partie.damier.deplacer(pos_source, pos_cible)
        self.canvas_damier.actualiser()
        self.pos_source_selectionnee = None
        self.pos_cible_selectionnee = None

        if self.partie.couleur_joueur_courant == "blanc":
            self.partie.couleur_joueur_courant = "noir"
        else:
            self.partie.couleur_joueur_courant = "blanc"

        self.joueur_en_cours()

    def nouvelle_partie(self):
        """ Méthode pour lancer une nouvelle partie. """

        self.partie = Partie()
        self.canvas_damier.damier = self.partie.damier
        self.canvas_damier.actualiser()
        self.messages['text'] = "Nouvelle partie commencée."
        self.pos_source_selectionnee = None
        self.pos_cible_selectionnee = None
        self.joueur_en_cours()

    def quitter_la_partie(self):
        """ Méthode permettant de quitter la fenêtre de la partie."""
        self.quit()

    def joueur_en_cours(self):
        """ Méthode permettant de savoir quel joueur a son tour actif et l'afficher sous forme de message

        À appeler à chaque fois qu'on veut mettre à jour le message.

        """

        couleur = self.partie.couleur_joueur_courant
        self.msg_couleur['foreground'] = 'black'
        self.msg_couleur['text'] = "C'est le tour du joueur {}".format(couleur)

    def trace(self):
        #Méthode temporaire
        source = self.pos_source_selectionnee
        cible = self.pos_cible_selectionnee
        self.msg_pos_source['foreground'] = 'black'
        self.msg_pos_source['text'] = "Position source : {}".format(source)
        self.msg_pos_cible['foreground'] = 'black'
        self.msg_pos_cible['text'] = "Position cible : {}".format(cible)
