# Script principal
from tkinter import * # Importation de tkinter pour l'interface graphique
from ajouter_lecture import *
import os
from editeur import * 

class Application(Tk):
    "Classe représentant une instance de l'application. Elle hérite de la classe Tk de tkinter"

    def __init__(self):
        "Constructeur de l'application"

        super().__init__() # On hérite de la classe Tk

        self.title("BookMinder") # Titre de la fenêtre d'application

        self.barre_menus = Menu(self, tearoff=0) # On ajoute une barre de menus à l'application 

        self.menu_lecture = Menu(self.barre_menus, tearoff=0) # On ajoute un menu lecture à la barre de menus. Il sert entre autre à ajouter un livre lu.

        self.menu_lecture.add_command(label="Nouvelle lecture...", command=lambda:FenetreAjouter(self)) # On ajoute une commande qui permet d'ajouter un livre dans les lectures au menu lecture

        self.menu_lecture.add_command(label="Ouvrir une lecture dans l'éditeur...", command=lambda:self.ouvrir_lecture(from_list=False, event=None))
        
        

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
                Label(self, text="Vos lectures (cliquez pour ouvrir dans l'éditeur):").pack(fill="both")
                self.lectures = Listbox(self) # Listbox contenant toutes les lectures ajoutées par l'utilisateur
                for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                    if fichier.startswith("chemin_"): # Si le nom du fichier commence par "chemin_"
                       f = open(f"paths/{fichier}", "r") # On veut lire le contenu du fichier
                       titre_livre = os.path.basename(f.read()) # On extrait le titre du livre depuis le chemin contenu dans le fichier texte
                       titre_fichier = fichier[7:] # Titre du livre comme il est contenu dans le fichier
                       titre_livre = titre_fichier
                       titre_livre = titre_livre.replace(".txt", "")
                               
                               

                                        
                           
                           
                       self.lectures.insert(END, titre_livre)
                       f.close() # On ferme le fichier texte

                self.lectures.pack(fill="both", expand=True)

                self.lectures.bind("<Double-1>", lambda event: self.ouvrir_lecture(from_list=True, event=event))

    def ouvrir_lecture(self, from_list, event):
        "Ouvrir une lecture depuis la liste graphique des lectures"
        if from_list: # Si l'utilisateur ouvre une lecture depuis la liste des lectures
            selection = self.lectures.nearest(event.y) # On obtient les éléments sélectionnés par la souris dans la Listbox
            print(selection)
            titre_clique = self.lectures.get(selection) # Titre sur lequel l'utilisateur a cliqué
            print("Vous avez cliqué(e) sur", titre_clique)
            for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                print(fichier)
            
                if fichier == f"chemin_{titre_clique}.txt": # Si le fichier correspond au titre cliqué
                    print("Le titre cliqué est dans le nom du fichier")
                    with open(f"paths/{fichier}", "r") as f: # On ouvre le fichier texte afin d'y trouver le chemin du fichier à ouvrir
                        chemin_fichier = f.read() # Chemin du fichier JSON à ouvrir
                        Editeur().ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin_fichier) # On ouvre le fichier JSON dans une nouvelle instance de l'éditeur
                        f.close()

        else: # Si l'utilisateur veut ouvrir une lecture depuis un autre endroit que la liste
            Editeur().ouvrir_fichier(event=None, dialogue=True) # Créer un nouvel éditeur et ouvrir le fichier dans celui-ci







        
        


    def titre(self, titre):
        "Changer le titre de la fenêtre"
        self.title(titre)            

app = Application() # On crée une nouvelle instance d'application

app.mainloop() # On exécute la boucle principale