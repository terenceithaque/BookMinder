# Script pour l'éditeur qui permet de modifier le fichier JSON d'une lecture
"L'éditeur de lecture est une fenêtre séparée dans laquelle l'utilisateur peut modifier ou ajouter des informations sur une lecture selon le principe de paires clé/valeur de JSON"
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Scrollbar as textscroll
import json
import os
import editorfuncs.copier_coller as copier # On importe le script copier_coller du dossier editorfuncs pour pouvoir copier des éléments
import editorfuncs.remplacer as remplacer # On importe le script remplacer pour remplacer du texte
import undo_redo


editeurs = [] # Liste des éditeurs ouverts


def chemin_ressource(chemin):
    "Trouver le chemin d'un fichier"
    try:
        base_path = sys._MEIPASS # PyInstaller crée un dossier temp et stocke les chemins dans _MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, chemin)     

class Editeur(Tk):
    "Classe représentant l'éditeur de lecture"
    def __init__(self, application_maitre):
        "Constructeur de l'éditeur"
        super().__init__() # On hérite des propriétés de la classe Tk


        editeurs.append(self) # On ajoute le nouvel éditeur à la liste des éditeurs ouverts


        self.app_maitre = application_maitre # Application maître

        

        self.text_scrollbar = textscroll(self) # Barre de défilement verticale pour le texte

        self.champ_texte = Text(self, yscrollcommand=self.text_scrollbar.set, undo=True) # Champ de texte dans lequel sont affichées les données d'un fichier JSON ouvert
        self.text_scrollbar.config(command=self.champ_texte.yview)
        self.text_scrollbar.pack(side=RIGHT, fill=Y)
        self.champ_texte.pack(fill="both", expand=True)

        self.title("Editeur de lecture")

        self.chemin_icone = chemin_ressource("app_icon.ico")

        self.iconbitmap(self.chemin_icone) # Icône de la fenêtre


        self.barre_menus = Menu(self, tearoff=0) # Barre de menus de l'éditeur


        self.file_saved = False # Savoir si les données ont été enregistrées dans un fichier

        self.menu_fichier = Menu(self, tearoff=0) # Menu "Fichier"

        self.fichier_ouvert = "" # Fichier ouvert dans l'éditeur

        self.fichier_existant = False # Variable pour savoir si le fichier ouvert existe ou non

        self.menu_fichier.add_command(label="Ouvrir une lecture... Ctrl+O", command=lambda:self.ouvrir_fichier(event=None, dialogue=True)) # Commande pour ouvrir un fichier JSON représentant une lecture

        
        
        
        self.menu_lectures_recentes = Menu(self.menu_fichier, tearoff=0) # Menu pour ouvrir une lecture récente
        if os.listdir("paths") != []: # Si le dossier paths n'est pas vide
            for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                f = open(f"paths/{fichier}", "r") # On veut lire le chemin contenu dans le fichier
                contenu_fichier = f.read() # Lire le fichier texte ouvert pour obtenir le chemin conduisant vers un fichier JSON représentant une lecture
                chemin_fichier_lecture = contenu_fichier + ".json"
                print(chemin_fichier_lecture)
                if os.path.exists(chemin_fichier_lecture): # Si le chemin contenu par le fichier existe
                    print(f"{chemin_fichier_lecture} existe")
                    self.menu_lectures_recentes.add_command(label=chemin_fichier_lecture, command=lambda chemin_fichier=chemin_fichier_lecture:Editeur(application_maitre).ouvrir_fichier(event=None,dialogue=False, nom_fichier=chemin_fichier))  # On ajoute un bouton pour ouvrir le fichier JSON correspondant dans un nouvel éditeur
                else:
                    print(f"{chemin_fichier_lecture} n'existe pas")
        self.menu_fichier.add_cascade(label="Lectures récentes", menu=self.menu_lectures_recentes) 

        self.menu_fichier.add_command(label="Enregistrer Ctrl + S", command=lambda:self.enregistrer(event=None))

        self.menu_fichier.add_command(label="Enregistrer sous...", command=self.enregistrer_sous)   


        self.menu_fichier.add_command(label="Quitter l'éditeur Ctrl + W", command=self.quitter) # Ajouter un bouton pour quitter l'éditeur


        self.menu_fichier.add_command(label="Quitter BookMinder... Ctrl + Q", command=application_maitre.quitter) # Bouton pour fermer Bookminder depuis l'éditeur
        self.barre_menus.add_cascade(label="Fichier", menu=self.menu_fichier)


        self.menu_edition = Menu(self, tearoff=0) # Menu "Edition"
        self.menu_edition.add_command(label="Remplacer", command=lambda:remplacer.afficher_dialogue_remplacer(self)) # Commande pour afficher la boîte de dialoge pour remplacer un texte 
        self.menu_edition.add_command(label="Annuler/Défaire Ctrl + Z", command=lambda:undo_redo.undo(self.champ_texte)) # L'utilisateur peut défaire la dernière action
        self.menu_edition.add_command(label="Refaire Ctrl + Y", command=lambda:undo_redo.redo(self.champ_texte)) # L'utilisateur peut refaire la dernière action
        self.menu_edition.add_command(label="Copier Ctrl + C", command=lambda:copier.copier(widget_texte=self.champ_texte)) # Commande pour copier du texte sélectionné 
        self.menu_edition.add_command(label="Copier tout Ctrl + Shift + C", command=lambda:copier.copier(widget_texte=self.champ_texte, all=True))
        self.menu_edition.add_command(label="Couper Ctrl + X", command=lambda:copier.couper(widget_texte=self.champ_texte)) # Commande pour couper du texte sélectionné
        self.menu_edition.add_command(label="Couper tout Ctrl + Shift + X", command=lambda:copier.couper(widget_texte=self.champ_texte, all=TRUE))
        self.menu_edition.add_command(label="Coller Ctrl+V", command=lambda:copier.coller(widget_texte=self.champ_texte)) # Commande pour coller un élément du presse-papiers
        self.barre_menus.add_cascade(label="Edition", menu=self.menu_edition)


        self.config(menu=self.barre_menus) # On configure la barre de menus comme menu de la fenêtre


        

        self.champ_texte.bind("<KeyRelease>", self.on_keyrelease) # Si une touche est pressée quand le champ de texte a le focus, faire toutes les actions nécessaires

        self.bind("<Control-o>", lambda event:self.ouvrir_fichier(event, dialogue=True))

        self.bind("<Control-s>", lambda event:self.enregistrer(event))

        self.bind("<Control-c>", lambda:copier.copier(widget_texte=self.champ_texte)) # L'utilisateur peut utiliser Ctrl + C pour copier du texte

        self.bind("<Control-Shift-C>", lambda event:copier.copier(event, widget_texte=self.champ_texte, all=True)) # L'utilisateur peut copier tout le texte d'un coup avec Ctrl+Shift+C
        self.bind("<Control-Shift-X>", lambda event:copier.couper(event, widget_texte=self.champ_texte, all=True)) # L'utilisateur peut couper tout le texte d'un coup avec Ctrl+Shift+X
        self.bind("<Control-x>", lambda:copier.couper(widget_texte=self.champ_texte)) # L'utilisateur peut utiliser Ctrl + X pour couper du texte

        self.bind("<Control-v>", lambda: copier.coller(widget_texte=self.champ_texte)) # L'utilisateur peut utiliser Ctrl + V pour coller du texte dans le champ de texte
        self.bind("<Control-w>", self.quitter)

        self.bind("<Control-q>", application_maitre.quitter)


        self.bind("<Control-z>", lambda event: undo_redo.undo(self.champ_texte)) # Défaire la dernière action 

        self.bind("<Control-y>", lambda event: undo_redo.redo(self.champ_texte)) # Refaire la dernière action

        self.raccourcis_claviers = ["<Control-o>", "<Control-s>"] # Liste des raccourcis clavier de l'éditeur

        self.protocol("WM_DELETE_WINDOW", self.quitter) # Si l'utilisateur clique sur le bouton en forme de croix pour quitter, on appelle self.quitter pour fermer proprement l'éditeur

        self.champ_texte.tag_add("test", 1.0)

        #self.champ_texte.tag_config("test", background="black")
    def ouvrir_fichier(self,event, dialogue=True, nom_fichier=""):
        "Ouvrir un fichier JSON représentant une lecture"
        if dialogue == True: # Si on doit afficher une boîte de dialogue pour demander à l'utilisateur de choisir un fichier à ouvrir
            nom_fichier = filedialog.askopenfilename(title="Sélectionnez un fichier JSON représentant une lecture :", filetypes=[("Base de données JSON", "*.json")]) # On demande à l'utilisateur de sélectionner le fichier à ouvrir
            self.fichier_ouvert = nom_fichier
            if nom_fichier:
                with open(nom_fichier, "r") as f: # On ouvre le fichier JSON en lecture
                    donnees = json.load(f) # Charger le fichier JSON en mémoire
                    #print(donnees)
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
                        #print("Données en JSON :", self.toJSON(donnees_affichees))
                        self.champ_texte.insert(END, donnees_affichees)

                        #donnees_formatees = donnees_formatees.decode("utf-8") # On décode les données formattées en utf-8

                       # print("Données formattées en utf-8 :", donnees_formatees) 
                        #self.after(0, self.champ_texte.insert, END, donnees_formatees)


            except FileNotFoundError:    # Si le fichier JSON n'existe pas
                messagebox.showerror("Le fichier n'existe pas ou plus", f"Le fichier {nom_fichier} n'existe pas ou plus") 


        self.title(f"{os.path.basename(nom_fichier)} - Editeur de lecture")

        self.fichier_existant = True # Le fichier existe



    def get_text(self):
        "Obtenir le texte contenu dans le champ"
        return self.champ_texte.get(1.0, END) # Retourner l'entièreté du contenu du champ de texte
    
    def on_keyrelease(self, event):
        "Gérer les fonctions à appeler lors de la pression des touches du clavier dans le champ de texte"
        self.mettre_a_jour_titre(event)   # Mettre à jour le titre de la fenêtre pour indiquer si des modifications ont été apportées



    def mettre_a_jour_titre(self, event):
        "Changer le titre de la fenêtre si une modification non enregistrée a été faite"

        if self.comparer_versions():   
                print("Il y a eu des modifications")
                if self.fichier_existant:
                    self.title(f"*{os.path.basename(self.fichier_ouvert)} - Editeur de lecture")

                else:
                    self.title(f"Fichier non enregistré - Editeur de lecture")

        else:
            #print("Il n'y a pas eu de modifications")
            self.title(f"{os.path.basename(self.fichier_ouvert)}")



    def afficherJSON(self):
        "Afficher le texte du champ converti en JSON"
        #print("texte du champ :", self.toJSON(self.champ_texte.get(1.0, END)))   





                   


    def toJSON(self, donnees):
        "Convertir des données dans un format JSON"
        lignes = donnees.split("\n") # Séparer les données par des lignes
        #print("Lignes :", lignes)
       

        cles = [] # Toutes les clés

        dict_donnees = {}

        derniere_cle = None # Dernière clé insérée dnas la liste

        for ligne in lignes: # Pour chaque ligne
            if ":" in ligne: # Si la ligne contient une paire clé/valeur
                parties = ligne.split(":") # On découpe la ligne au niveay de la paire
                if len(parties[0].split()) == 1: # On ne prend la clé que si elle est en un seul mot
                    cle = parties[0]
                    #print("Clé courante :", cle)
                    cles.append(cle) # On ajoute la clé à la liste
                    #print("Toutes les clés:", cles)

                else: # Si la clé n'est pas en un seul mot
                    derniere_cle = cles[len(cles) -1] # On prend la dernière clé qui a été ajoutée
                    cle = derniere_cle

                if len(parties) > 1: # Si la ligne a été découpée en plus de deux parties
                    valeur = parties[1] # On enregistre la valeur de chaque clé dans une variable
                    #print("Valeur de la clé :", valeur)
                    if cle != derniere_cle: # Si la clé ne correspond pas à la dernière insérée
                        dict_donnees[cle] = valeur

                    else: # Sinon
                        dict_donnees[cle] += valeur   # On met à jour l'ancienne clé       

                            
                        

                    


            


        #print("Résumé dans le dictionnaire :", dict_donnees["resume"])
        donnees_json = json.dumps(dict_donnees, indent=4)
        #print("Données json :", donnees_json)
        return donnees_json, dict_donnees    



        


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
    

    def modifications_sauvegardees(self):
        "Vérifier si les modifications apportées à un fichier ont été sauvegardées"
        if self.comparer_versions(): # Si des modifications ont été faites
            return False
        
        return True # Si l'utilisateur n'a pas fait de modifications, on renvoie True


    def comparer_versions(self):
        "Comparer la version enregistrée et la version en cours de travail d'un fichier"
        if self.fichier_existant and self.fichier_ouvert != "":
           # print("Le fichier existe et est ", self.fichier_ouvert)
            with open(self.fichier_ouvert, encoding="utf-8",  mode="r") as f: # On ouvre le fichier JSON en lecture
                version_enregistree = json.load(f) # Version enregistrée du fichier 
                f.close()

    
            version_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier

            version_enregistree_json = json.dumps(version_enregistree, sort_keys=True)
            version_travail_json = json.dumps(version_travail, sort_keys=True)
            
            #print("Version enregistrée (json) :", version_enregistree_json)
            #print("Version de travail (json) :", version_travail_json)
            return version_travail_json != version_enregistree_json
        
        else: # Si l'utilisateur travaille sur un nouveau fichier
            #print("Le fichier n'existe pas")
            version_enregistree = "" # Le contenu de la version enregistrée du fichier est vide car elle n'existe pas
            version_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier
            return version_travail != version_enregistree
        


    def enregistrer_sous(self):
        "Enregistrer le contenu du champ de texte dans un nouveau fichier au format JSON"
        try:

            donnees = self.toJSON(self.champ_texte.get(1.0, END))[1] # On formate les données contenues dans le champ de texte au format JSON
            localisation_fichier = filedialog.asksaveasfilename(title="Où souhaitez-vous enregistrer le fichier ?", filetypes=[("Base de données JSON", "*.json")], defaultextension=".json")  # Demander à l'utilisateur où il souhaite enregistrer le fichier
            if localisation_fichier != "": # Si l'utilisateur n'a pas cliqué sur Annuler
                self.fichier_ouvert = localisation_fichier
                with open(self.fichier_ouvert, "w", encoding="utf-8") as f: # On ouvre le fichier en écriture
                    json.dump(donnees, f, indent=4)
                    f.close() # On ferme le fichier


                    self.fichier_existant = True # Maintenant, le fichier existe


                    if "Lectures favorites BookMinder" in localisation_fichier: # Si le fichier est enregistré dans les favoris
                        self.app_maitre.actualiser_menu_favoris() # Mettre à jour le menu des favoris

                    self.title(f"{os.path.basename(self.fichier_ouvert)}")

                    self.file_saved = True # Les données ont été enregistrées dans un fichier
            
            

        except FileNotFoundError:
            pass


         
    
    def enregistrer(self, event=None):
        "Enregistrer les modifications faites à un fichier JSON"
        if not self.fichier_existant or self.fichier_ouvert == "": # Si l'utilisateur n'a pas enregistré les données dans un fichier ou que le fichier n'est pas ouvert
            if not self.fichier_existant: # Si le fichier n'existe pas
                print("Les données n'ont pas été enregistrées sous forme de fichier")

            if self.fichier_ouvert == "": # Si l'utilisateur n'a ouvert aucun fichier
                print("Aucun fichier n'a été ouvert")  
            if not self.file_saved: # Si les données n'ont pas été enregistrées dans un fichier
                self.enregistrer_sous()

        else:
            if self.comparer_versions(): # Si des modifications ont été faites au fichier
                with open(self.fichier_ouvert,encoding="utf-8", mode= "r") as f: # On ouvre le fichier JSON en lecture 
                    self.donnees_enregistrees = json.load(f) # On charge les données enregistrées
                    f.close() # On ferme le fichier

            donnees_travail = self.toJSON(self.champ_texte.get(1.0, END))[1] # Version en cours de travail du fichier

            self.donnees_enregistrees= dict(donnees_travail) # On met à jour les données enregistrées sur la version en cours de travail

            with open(self.fichier_ouvert, "w", encoding="utf-8") as f: # On ouvre le fichier JSON en écriture
                json.dump(self.donnees_enregistrees, f, indent=4)
                f.close()       

        #self.title(f"{os.path.basename(self.fichier_ouvert)}")
                
        self.mettre_a_jour_titre(event=None) # Mettre à jour le titre de la fenêtre


    def quitter(self, event=None):
        "Quitter l'éditeur"
        if not self.modifications_sauvegardees(): # Si l'utilisateur n'a pas sauvegardé les modifications apportées à un fichier
            enregistrer = messagebox.askyesnocancel("Enregistrer les modifications ?", "Les dernières modifications n'ont pas été enregistrées. Voulez-vous les enregistrer avant de quitter ?") # Demander à l'utilisateur s'il souhaite enregistrer les modifications
            if enregistrer == True: # Si l'utilisateur veut enregistrer les modifications
                self.enregistrer() # Enregistrer les modifications
                self.destroy() # Détruire la fenêtre de l'éditeur
                editeurs.remove(self) # On retire l'éditeur actuel des éditeurs ouverts

            elif enregistrer == False: # Si l'utilisateur ne veut pas enregistrer les modifications
                self.destroy() # On a juste à détruire la fenêtre de l'éditeur
                editeurs.remove(self)

        else: # Si les modifications ont été sauvegardées
            self.destroy() # Détruire la fenêtre de l'éditeur 
            editeurs.remove(self)           


            






    



#edit = Editeur()
#edit.ouvrir_fichier(dialogue=False, nom_fichier=r"C:\Données\Térence\198.json")
#edit.mainloop()           


                        


