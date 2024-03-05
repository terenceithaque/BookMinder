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

        self.fichier_ouvert = "" # Fichier ouvert dans l'éditeur

        self.fichier_existant = False # Variable pour savoir si le fichier ouvert existe ou non

        self.menu_fichier.add_command(label="Ouvrir une lecture...", command=lambda:self.ouvrir_fichier(event=None, dialogue=True)) # Commande pour ouvrir un fichier JSON représentant une lecture

        
        
        self.menu_lectures_recentes = Menu(self.menu_fichier, tearoff=0) # Menu pour ouvrir une lecture récente
        if os.listdir("paths") != []: # Si le dossier paths n'est pas vide
            for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                f = open(f"paths/{fichier}", "r") # On veut lire le chemin contenu dans le fichier
                chemin_fichier_lecture = f.read() # Lire le fichier texte ouvert pour obtenir le chemin conduisant vers un fichier JSON représentant une lecture
                chemin_fichier_lecture += ".json" # On ajoute l'extension du fichier JSON
                self.menu_lectures_recentes.add_command(label=chemin_fichier_lecture, command=lambda chemin_fichier=chemin_fichier_lecture:Editeur().ouvrir_fichier(event=None,dialogue=False, nom_fichier=chemin_fichier))  # On ajoute un bouton pour ouvrir le fichier JSON correspondant dans un nouvel éditeur

        self.menu_fichier.add_cascade(label="Lectures récentes", menu=self.menu_lectures_recentes) 

        self.menu_fichier.add_command(label="Enregistrer Ctrl + S", command=lambda:self.enregistrer(event=None))

        self.menu_fichier.add_command(label="Enregistrer sous...", command=self.enregistrer_sous)   

        self.barre_menus.add_cascade(label="Fichier", menu=self.menu_fichier)


        self.config(menu=self.barre_menus) # On configure la barre de menus comme menu de la fenêtre

        self.champ_texte = Text(self) # Champ de texte dans lequel sont affichées les données d'un fichier JSON ouvert

        self.champ_texte.pack(fill="both", expand=True)

        self.champ_texte.bind("<KeyRelease>", self.mettre_a_jour_titre) # Si une modification a été faite dans le champ de texte, on change le titre de la fenêtre pour indiquer qu'elle n'a pas été enregistrée

        self.bind("<Control-o>", lambda event:self.ouvrir_fichier(event, dialogue=True))

        self.bind("<Control-s>", lambda event:self.enregistrer(event))


        self.raccourcis_claviers = ["<Control-o>", "<Control-s>"] # Liste des raccourcis clavier de l'éditeur


    def ouvrir_fichier(self,event, dialogue=True, nom_fichier=""):
        "Ouvrir un fichier JSON représentant une lecture"
        if dialogue == True: # Si on doit afficher une boîte de dialogue pour demander à l'utilisateur de choisir un fichier à ouvrir
            nom_fichier = filedialog.askopenfilename(title="Sélectionnez un fichier JSON représentant une lecture :", filetypes=[("Base de données JSON", "*.json")]) # On demande à l'utilisateur de sélectionner le fichier à ouvrir
            self.fichier_ouvert = nom_fichier
            if nom_fichier:
                with open(nom_fichier, "r") as f: # On ouvre le fichier JSON en lecture
                    donnees = json.load(f) # Charger le fichier JSON en mémoire
                    print(donnees)
                    f.close() # On ferme le fichier JSON

                    donnees_formatees = json.dumps(donnees, indent=4, ensure_ascii=False) # Données du fichier JSON formattées sous forme de chaîne de caractères normale
                    donnees_affichees = "\n".join(f"{key}:{value}" for key, value in donnees.items()) # Données formatées telles qu'elles sont affichées dans le champ de texte
                    
        
                    self.champ_texte.insert(END, donnees_affichees)

                  

        if dialogue == False: # Si on ne doit pas afficher de dialogue
            try :
                if nom_fichier: 
                    
                    if ".json" not in nom_fichier:
                        nom_fichier += ".json"

                    self.fichier_ouvert = nom_fichier    
                    with open(nom_fichier, "r", encoding="utf-8") as f: # On ouvre le fichier JSON en lecture
                        donnees = json.load(f) # On charge le fichier JSON en mémoire
                        print(donnees)
                        f.close() # On ferme le fichier JSON 

                        donnees_formatees = json.dumps(donnees, indent=4, ensure_ascii=False)   # Données du fichier JSON formattées sous forme de chaîne de caractères normale
                        donnees_affichees = "\n".join(f"{key}:{value}" for key, value in donnees.items()) # Données formatées telles qu'elles sont affichées dans le champ de texte
                        print("Données en JSON :", self.toJSON(donnees_affichees))
                        self.champ_texte.insert(END, donnees_affichees)

                        #donnees_formatees = donnees_formatees.decode("utf-8") # On décode les données formattées en utf-8

                        print("Données formattées en utf-8 :", donnees_formatees) 
                        #self.after(0, self.champ_texte.insert, END, donnees_formatees)


            except FileNotFoundError:    # Si le fichier JSON n'existe pas
                messagebox.showerror("Le fichier n'existe pas ou plus", f"Le fichier {nom_fichier} n'existe pas ou plus") 


        self.title(f"{os.path.basename(nom_fichier)} - Editeur de lecture")

        self.fichier_existant = True # Le fichier existe


    def mettre_a_jour_titre(self, event):
        "Changer le titre de la fenêtre si une modification non enregistrée a été faite"

        if self.comparer_versions():   
                print("Il y a eu des modifications")
                if self.fichier_existant:
                    self.title(f"*{os.path.basename(self.fichier_ouvert)} - Editeur de lecture")

                else:
                    self.title(f"Fichier non enregistré - Editeur de lecture")

        else:
            print("Il n'y a pas eu de modifications")
            self.title(f"{os.path.basename(self.fichier_ouvert)}")



                   


    def toJSON(self, donnees):
        "Convertir des données dans un format JSON"
        lignes = donnees.split("\n") # Séparer les données par des lignes

        dict_donnnees = {} # Dictionnaire pour les clés et valeurs de chaque donnée

        for ligne in lignes: # Pour chaque ligne
            parties = ligne.split(":", 1) # Séparer chaque ligne en clés et valeurs

            if len(parties) == 2:
                cle, valeur = parties

                cle = cle.strip()
                valeur = valeur.strip()

                dict_donnnees[cle] = valeur

        donnees_json = json.dumps(dict_donnnees, indent=4)
        return donnees_json, dict_donnnees    



        


    """def verifier_modifications(self):
        "Comparer les modifications entre la version enregistrée et la version en cours de travail d'un fichier JSON"
        with open(self.fichier_ouvert, "r") as f: # On ouvre le fichier JSON en lecture
            version_enregistree = f.read() # On lit le fichier pour obtenir le contenu enregistré du fichier
            print("Version enregistrée :", version_enregistree)
            version_travail = self.toJSON(self.champ_texte.get(1.0, END))[0] # Version en cours de travail du fichier, avec les modifications
            print("Version en cours de travail :", version_travail)
            
            version_enregistree_normalisee = json.dumps(json.loads(version_enregistree), sort_keys=True) # Normaliser les chaînes de caractères JSON en retirant les espaces blancs et en triant les clés
            
            if version_travail != version_enregistree:
                return True
            
        return False"""


    def comparer_versions(self):
        "Comparer la version enregistrée et la version en cours de travail d'un fichier"
        if self.fichier_existant and self.fichier_ouvert != "":
            print("Le fichier existe et est ", self.fichier_ouvert)
            with open(self.fichier_ouvert, "r") as f: # On ouvre le fichier JSON en lecture
                version_enregistree = json.load(f) # Version enregistrée du fichier 
                f.close()

    
            version_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier

            version_enregistree_json = json.dumps(version_enregistree, sort_keys=True)
            version_travail_json = json.dumps(version_travail, sort_keys=True)
            
            print("Version enregistrée (json) :", version_enregistree_json)
            print("Version de travail (json) :", version_travail_json)
            return version_travail_json != version_enregistree_json
        
        else: # Si l'utilisateur travaille sur un nouveau fichier
            print("Le fichier n'existe pas")
            version_enregistree = "" # Le contenu de la version enregistrée du fichier est vide car elle n'existe pas
            version_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier
            return version_travail != version_enregistree
        


    def enregistrer_sous(self):
        "Enregistrer le contenu du champ de texte dans un nouveau fichier au format JSON"
        try:
            donnees = self.toJSON(self.champ_texte.get(1.0, END))[1] # On formate les données contenues dans le champ de texte au format JSON
            localisation_fichier = filedialog.asksaveasfilename(title="Où souhaitez-vous enregistrer le fichier ?", filetypes=[("Base de données JSON", "*.json")], defaultextension=".json")  # Demander à l'utilisateur où il souhaite enregistrer le fichier
            self.fichier_ouvert = localisation_fichier
            with open(self.fichier_ouvert, "w") as f: # On ouvre le fichier en écriture
                json.dump(donnees, f, indent=4)
                f.close() # On ferme le fichier


                self.fichier_existant = True # Maintenant, le fichier existe

                self.title(f"{os.path.basename(self.fichier_ouvert)}")

        except FileNotFoundError:
            pass


         
    
    def enregistrer(self, event=None):
        "Enregistrer les modifications faites à un fichier JSON"
        if not self.fichier_existant: # Si l'utilisateur n'a pas enregistré les données dans un fichier ou que le fichier n'est pas ouvert
            self.enregistrer_sous()

        else:
            if self.comparer_versions(): # Si des modifications ont été faites au fichier
                with open(self.fichier_ouvert, "r") as f: # On ouvre le fichier JSON en lecture 
                    self.donnees_enregistrees = json.load(f) # On charge les données enregistrées
                    f.close() # On ferme le fichier

            donnees_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier

            self.donnees_enregistrees= dict(donnees_travail) # On met à jour les données enregistrées sur la version en cours de travail

            with open(self.fichier_ouvert, "w") as f: # On ouvre le fichier JSON en écriture
                json.dump(self.donnees_enregistrees, f, indent=4)
                f.close()       

        #self.title(f"{os.path.basename(self.fichier_ouvert)}")
                
        self.mettre_a_jour_titre(event=None) # Mettre à jour le titre de la fenêtre


            






    



#edit = Editeur()
#edit.ouvrir_fichier(dialogue=False, nom_fichier=r"C:\Données\Térence\198.json")
#edit.mainloop()           


                        


