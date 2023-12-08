# Auteurs: À compléter

from tkinter import Tk, Label, NSEW, Button
from Partie2.canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position

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

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # les Attributes ajoute par étudiant
        self.position_cible_courante = None

        self.position_cible_courante = None

        # Affiche un message si le joueur doit prendre une pièce
        self.msg_prendre = Label(self)
        self.msg_prendre.grid()

        # Affiche un message si le joueur faire un clic invalide
        # self.msg_invalide = Label(self)
        # self.msg_invalide.grid()

        # Affiche le nom du joueur qui joue actuellement
        self.msg_couleur = Label(self)
        self.msg_couleur.grid()

        # Appel initial pour afficher la couleur du joueur
        self.joueur_en_cours()

        # Affiche un bouton pour quitter la partie
        self.bouton_quitter = Button(self, text="Quitter la partie", command=self.quitter_la_partie)
        self.bouton_quitter.grid(row=0, column=1, sticky='ne', padx=10, pady=10)

        # Affiche un bouton pour lancer une nouvelle partie
        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.grid(row=0, column=1, sticky='ne', padx=10, pady=40)

        # Initialisation de la fin de partie
        self.partie_terminee()

        self.message_prendre()

        # self.message_invalide()

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

        if self.canvas_damier.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
            self.partie.doit_prendre = True

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)

        if piece is None:
            if self.partie.position_source_selectionnee is None:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'

            else:
                cible_valide, msg_erreur = self.partie.position_cible_valide(position)

                if cible_valide:
                    deplacement = self.canvas_damier.damier.deplacer(self.partie.position_source_selectionnee, position)

                    if deplacement == "prise" and self.canvas_damier.damier.piece_peut_faire_une_prise(position):
                        self.partie.doit_prendre = True
                        self.partie.position_source_forcee = position
                        self.partie.position_source_selectionnee = None
                        self.messages['text'] = ''
                        self.messages['foreground'] = 'black'
                        self.canvas_damier.actualiser()

                    else:
                        self.canvas_damier.actualiser()
                        self.change_joueur()
                        self.reset_tour()

                else:
                    self.messages['text'] = msg_erreur
                    self.messages['foreground'] = 'red'
                    self.reset_tour()
        else:
            if self.partie.position_source_selectionnee is None or piece.couleur == self.partie.couleur_joueur_courant:
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)

                source_valide, msg_erreur = self.partie.position_source_valide(position)

                if source_valide:
                    self.partie.position_source_selectionnee = position
                else:
                    self.messages['text'] = msg_erreur
                    self.messages['foreground'] = 'red'

        # print("self.partie.doit_prendre:", self.partie.doit_prendre)
        # print("self.partie.position_source_forcee:", self.partie.position_source_forcee)
        # print("self.partie.position_source_selectionnee:", self.partie.position_source_selectionnee)

        self.joueur_en_cours()
        self.message_prendre()

        # self.message_invalide()

    def reset_tour(self):
        self.partie.position_source_selectionnee = None
        self.messages['text'] = ''
        self.messages['foreground'] = 'black'
        self.partie.doit_prendre = False
        self.partie.position_source_forcee = None

    def change_joueur(self):
        if self.partie.couleur_joueur_courant == "blanc":
            self.partie.couleur_joueur_courant = "noir"
        else:
            self.partie.couleur_joueur_courant = "blanc"

    def nouvelle_partie(self):
        """ Méthode pour lancer une nouvelle partie. """

        self.partie = Partie()
        self.canvas_damier.damier = self.partie.damier
        self.canvas_damier.actualiser()
        self.messages['text'] = "Nouvelle partie commencée."
        self.partie.position_source_selectionnee = None
        self.position_cible_courante = None
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

    def partie_terminee(self):

        if not self.partie.damier.piece_de_couleur_peut_se_deplacer(self.partie.couleur_joueur_courant) and \
                not self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):

            if self.partie.couleur_joueur_courant == "blanc":
                gagnant = "noir"
            else :
                gagnant = "blanc"

            messagebox.showinfo("Fin de partie", f"Le joueur {gagnant} a gagné!")
            self.quitter_la_partie()

        else:
            self.after(100, self.partie_terminee)

    def message_prendre(self):

        if self.partie.doit_prendre == True:
            self.msg_prendre['foreground'] = 'black'
            self.msg_prendre['text'] = f"Le joueur doit prendre une pièce."
        else :
            self.msg_prendre['foreground'] = 'black'
            self.msg_prendre['text'] = ''

    # def message_invalide(self):
    #
    #     if self.partie.doit_prendre and self.partie.position_source_forcee is not None:
    #         if self.partie.position_source_selectionnee != self.partie.position_source_forcee:
    #             self.msg_invalide['foreground'] = 'red'
    #             self.msg_invalide['text'] = 'Vous pouvez prendre une pièce avec une autre pièce.'
