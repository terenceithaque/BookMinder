# Script pour ajouter une lecture
from tkinter import * # Importation de tkinter pour l'interface graphique
from tkinter import filedialog # Importation du module filedialog de tkinter pour dialoguer avec les fichiers
from resume import * 


class FenetreAjouter(Toplevel):
    "Classe représentant une fenêtre permettant d'ajouter une lecture"
    def __init__(self, fenetre_maitre):
        "Constructeur de FenetreAjouter"
        super().__init__() # On hérite de la classe Toplevel de tkinter

        self.fenetre_maitre = fenetre_maitre # Fenêtre maître

        self.label_titre = Label(self, text="Titre du livre :") # Label pour demander à l'utilisateur de saisir le titre du livre

        self.label_titre.pack(fill="both")

        self.titre_livre = Entry(self) # Entrée pour saisir le titre du livre

        self.titre_livre.pack(fill="both")

        self.label_annee = Label(self, text="Année de publication :") # Label pour demander à l'utilisateur de saisir l'année de publication du livre (optionnel)
        self.label_annee.pack(fill="both")

        self.annee_livre = Entry(self) # Entrée pour saisir l'année de publication du livre
        self.annee_livre.pack(fill="both")

        self.label_auteur = Label(self, text="Auteur(e) du livre :") # Label pour demander à l'utilisateur de saisir l'auteur(e) du livre (optionnel)
        self.label_auteur.pack(fill="both")

        self.auteur_livre = Entry(self)  # Entrée pour saisir le nom de l'auteur(e) du livre
        self.auteur_livre.pack(fill="both")

