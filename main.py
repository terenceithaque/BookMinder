# Script principal
from tkinter import * # Importation de tkinter pour l'interface graphique
from ajouter_lecture import *
import os
from editeur import * 
import keyboard

class Application(Tk):
    "Classe représentant une instance de l'application. Elle hérite de la classe Tk de tkinter"

    def __init__(self):
        "Constructeur de l'application"

        super().__init__() # On hérite de la classe Tk

        self.title("BookMinder") # Titre de la fenêtre d'application

        self.barre_menus = Menu(self, tearoff=0) # On ajoute une barre de menus à l'application 

        self.menu_lecture = Menu(self.barre_menus, tearoff=0) # On ajoute un menu lecture à la barre de menus. Il sert entre autre à ajouter un livre lu.

        self.menu_lecture.add_command(label="Nouvelle lecture... Ctrl + N", command=lambda:FenetreAjouter(self)) # On ajoute une commande qui permet d'ajouter un livre dans les lectures au menu lecture

        keyboard.add_hotkey("Ctrl + N", lambda:FenetreAjouter(self))


        

        self.barre_menus.add_cascade(label="Lecture", menu=self.menu_lecture) # On insère le menu lecture dans la barre de menus

        self.menu_editeur = Menu(self, tearoff=0) # Menu "Editeur"
        self.menu_editeur.add_command(label="Ouvrir l'éditeur de lecture", command=lambda:Editeur())  # Commande pour lancer une nouvelle instance de l'éditeur de lectures
        
        self.barre_menus.add_cascade(label="Editeur", menu=self.menu_editeur)

        self.config(menu = self.barre_menus) # On configure le menu de la fenêtre comme étant la barre de menus qu'on a créée

        if os.path.exists("paths"): # Si le dossier paths existe
            if os.listdir("paths") == []: # Si le dossier paths est vide, alors on considère qu'aucune lecture n'a été enregistrée
                Label(self, text="Vous n'avez enregistré(e) aucune lecture.").pack(fill="both") # On affiche un texte pour avertir l'utilisateur qu'il n'a enregistré aucune lecture
                self.bouton_ajouter_lecture = Button(self, text="Ajouter une nouvelle lecture...", command=lambda:FenetreAjouter(self)) # On ajoute un bouton pour permettre à l'utilisateur d'ajouter une nouvelle lecture
                self.bouton_ajouter_lecture.pack()


            else:
                Label(self, text="Vos lectures :").pack(fill="both")
                self.lectures = Listbox(self) # Listbox contenant toutes les lectures ajoutées par l'utilisateur
                for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                    if fichier.startswith("chemin_"): # Si le nom du fichier commence par "chemin_"
                       f = open(f"paths/{fichier}", "r") # On veut lire le contenu du fichier
                       titre_livre = os.path.basename(f.read()) # On extrait le titre du livre depuis le chemin contenu dans le fichier texte
                       self.lectures.insert(END, titre_livre)
                       f.close() # On ferme le fichier texte

                self.lectures.pack(fill="both", expand=True)


    def titre(self, titre):
        "Changer le titre de la fenêtre"
        self.title(titre)            

app = Application() # On crée une nouvelle instance d'application

app.mainloop() # On exécute la boucle principale