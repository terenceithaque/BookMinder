# Script pour l'éditeur qui permet de modifier le fichier JSON d'une lecture
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import json
import os


class Editeur(Tk):
    "Classe représentant l'éditeur de lecture"
    def __init__(self):
        "Constructeur de l'éditeur"
        super().__init__() # On hérite des propriétés de la classe Tk

        self.title("Editeur de lecture")

        self.barre_menus = Menu(self, tearoff=0) # Barre de menus de l'éditeur

        self.menu_fichier = Menu(self, tearoff=0) # Menu "Fichier"

        self.menu_fichier.add_command(label="Ouvrir une lecture...", command=lambda:self.ouvrir_fichier(dialogue=True)) # Commande pour ouvrir un fichier JSON représentant une lecture

        self.menu_lectures_recentes = Menu(self.menu_fichier, tearoff=0) # Menu pour ouvrir une lecture récente
        if os.listdir("paths") != []: # Si le dossier paths n'est pas vide
            for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                f = open(f"paths/{fichier}", "r") # On veut lire le chemin contenu dans le fichier
                chemin_fichier_lecture = f.read() # Lire le fichier texte ouvert pour obtenir le chemin conduisant vers un fichier JSON représentant une lecture
                chemin_fichier_lecture += ".json" # On ajoute l'extension du fichier JSON
                self.menu_lectures_recentes.add_command(label=chemin_fichier_lecture, command=lambda chemin_fichier=chemin_fichier_lecture:self.ouvrir_fichier(dialogue=False, nom_fichier=chemin_fichier))  # On ajoute un bouton pour ouvrir le fichier JSON correspondant dans un nouvel éditeur

        self.menu_fichier.add_cascade(label="Lectures récentes", menu=self.menu_lectures_recentes)    

        self.barre_menus.add_cascade(label="Fichier", menu=self.menu_fichier)


        self.config(menu=self.barre_menus) # On configure la barre de menus comme menu de la fenêtre

        self.champ_texte = Text(self) # Champ de texte dans lequel sont affichées les données d'un fichier JSON ouvert

        self.champ_texte.pack(fill="both", expand=True)

    def ouvrir_fichier(self, dialogue=True, nom_fichier=""):
        "Ouvrir un fichier JSON représentant une lecture"
        if dialogue == True: # Si on doit afficher une boîte de dialogue pour demander à l'utilisateur de choisir un fichier à ouvrir
            nom_fichier = filedialog.askopenfilename(title="Sélectionnez un fichier JSON représentant une lecture :", filetypes=[("Base de données JSON", "*.json")]) # On demande à l'utilisateur de sélectionner le fichier à ouvrir
            if nom_fichier:
                with open(nom_fichier, "r") as f: # On ouvre le fichier JSON en lecture
                    donnees = json.load(f) # Charger le fichier JSON en mémoire
                    print(donnees)
                    f.close() # On ferme le fichier JSON

                    donnees_formatees = json.dumps(donnees, indent=4) # Données du fichier JSON formattées sous forme de chaîne de caractères normale
                    self.champ_texte.insert(END, donnees_formatees)

        if dialogue == False: # Si on ne doit pas afficher de dialogue
            try :
                if nom_fichier: 
                    if ".json" not in nom_fichier:
                        nom_fichier += ".json"
                    with open(nom_fichier, "r", encoding="utf-8") as f: # On ouvre le fichier JSON en lecture
                        donnees = json.load(f) # On charge le fichier JSON en mémoire
                        print(donnees)
                        f.close() # On ferme le fichier JSON 

                        donnees_formatees = json.dumps(donnees, indent=4, ensure_ascii=False)   # Données du fichier JSON formattées sous forme de chaîne de caractères normale


                        #donnees_formatees = donnees_formatees.decode("utf-8") # On décode les données formattées en utf-8

                        print("Données formattées en utf-8 :", donnees_formatees) 
                        self.champ_texte.insert(END, donnees_formatees)


            except FileNotFoundError:    # Si le fichier JSON n'existe pas
                messagebox.showerror("Le fichier n'existe pas ou plus", f"Le fichier {nom_fichier} n'existe pas ou plus") 


        self.title(f"{os.path.basename(nom_fichier)} - Editeur de lecture")             


#edit = Editeur()
#edit.ouvrir_fichier(dialogue=False, nom_fichier=r"C:\Données\Térence\198.json")
#edit.mainloop()                           


