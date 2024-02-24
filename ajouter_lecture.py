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
