# Script principal
from tkinter import * # Importation de tkinter pour l'interface graphique
from tkinter.ttk import Scrollbar
from tkinter import messagebox
from ajouter_lecture import *
import os
from editeur import * 
from favoris import *
import sys


def chemin_ressource(chemin):
    "Trouver le chemin d'un fichier"
    try:
        base_path = sys._MEIPASS # PyInstaller crée un dossier temp et stocke les chemins dans _MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, chemin)        

class Application(Tk):
    "Classe représentant une instance de l'application. Elle hérite de la classe Tk de tkinter"

    def __init__(self):
        "Constructeur de l'application"

        super().__init__() # On hérite de la classe Tk

        self.protocol("WM_DELETE_WINDOW", self.quitter) # Si l'utilisateur clique sur le bouton en forme de croix pour quitter, on appelle self.quitter pour fermer proprement l'application


        self.titres = [] # Liste des titres enregistrés

        self.chemin_icone = chemin_ressource("app_icon.ico")

        self.iconbitmap(self.chemin_icone) # Icône de la fenêtre d'application

        self.title("BookMinder") # Titre de la fenêtre d'application

        self.barre_menus = Menu(self, tearoff=0) # On ajoute une barre de menus à l'application 

        self.menu_lecture = Menu(self.barre_menus, tearoff=0) # On ajoute un menu lecture à la barre de menus. Il sert entre autre à ajouter un livre lu.

        self.menu_lecture.add_command(label="Nouvelle lecture... Ctrl + N", command=lambda:FenetreAjouter(self, self.raifraichir_liste_lecture)) # On ajoute une commande qui permet d'ajouter un livre dans les lectures au menu lecture

        self.menu_lecture.add_command(label="Ouvrir une lecture dans l'éditeur... Ctrl + O", command=lambda:self.ouvrir_lecture(from_list=False, event=None))
        
        self.menu_lecture.add_command(label="Quitter l'application... Ctrl + Q", command=self.quitter)
        

        self.barre_menus.add_cascade(label="Lecture", menu=self.menu_lecture) # On insère le menu lecture dans la barre de menus


        self.menu_editeur = Menu(self, tearoff=0) # Menu "Editeur"
        self.menu_editeur.add_command(label="Ouvrir l'éditeur de lecture  F1", command=lambda:Editeur(self))  # Commande pour lancer une nouvelle instance de l'éditeur de lectures
        
        self.barre_menus.add_cascade(label="Editeur", menu=self.menu_editeur)


        self.menu_favoris = Menu(self, tearoff=0) # Menu pour gérer les lectures favorites
        self.menu_favoris.add_command(label="Créer un dossier Lectures favorites BookMinder", command=self.demander_creer_favoris) # Commande pour créer un dossier de favoris
        self.emplacement_favoris = emplacement_favoris() # Emplacement des lectures favorites
        #self.favoris = [] # Liste des favoris
        if lister_lectures_favorites() is not [] and self.emplacement_favoris is not None:
                for dirpath, dirnames, filenames in os.walk(self.emplacement_favoris): # Pour chaque dossier et fichier du dossier des favoris
                    for dir in dirnames:
                        for element in os.listdir(self.emplacement_favoris): # Pour chaque fichier de lectures
                            
                            fichier_ajoute = False # Savoir le chemin du fichier a été ajouté au menu
                            chemin_lecture = os.path.join(dirpath, element)
                            if os.path.isfile(chemin_lecture): # Si l'élément est un fichier
                               
                                if not fichier_ajoute:
                                    self.menu_favoris.add_command(label=chemin_lecture, command=lambda chemin_lecture=chemin_lecture: Editeur(self).ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin_lecture)) # Commande pour ouvrir une lecture favorite dans l'éditeur
                                    fichier_ajoute = True

                    for dir in dirnames:    # Pour chaque dossier
                        menu_dossier = Menu(self.menu_favoris,  tearoff=0) # Ajouter un menu contenant les lectures présentes dans le dossier
                        chemin_dossier = os.path.join(dirpath, dir)
                        for file in os.listdir(chemin_dossier): # Pour chaque fichier du dossier
                            print(file)
                            chemin_lecture = os.path.join(chemin_dossier, file) # Joindre le dossier du fichier et le fichier lui-même afin de former un chemin
                            menu_dossier.add_command(label=chemin_lecture, command=lambda chemin_lecture=chemin_lecture: Editeur(self).ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin_lecture))
                            menu_dossier
                        self.menu_favoris.add_cascade(label=dir, menu=menu_dossier)     

        self.barre_menus.add_cascade(label="Favoris", menu=self.menu_favoris)

        self.label_rechercher = Label(self, text="Rechercher une lecture :") # Label indiquant à l'utilisateur qu'il peut rechercher une lecture
        self.label_rechercher.pack(fill="both")

        self.recherche = Entry(self) # Entrée pour saisir une lecture à rechercher

        self.recherche.pack(fill="both")

        self.recherche.bind("<KeyRelease>", self.rechercher_lecture) # On appelle la fonction de recherche à chaque fois que l'utilisateur saisit quelque chose dans la barre de recherche

        self.bouton_rafraichir = Button(self, text="Rafraîchir la liste de lecture (Ctrl + R ou F5)", command=self.raifraichir_liste_lecture)

        self.bouton_rafraichir.pack()

        self.menu_contextuel = Menu(self, tearoff=0) # Menu contextuel de la liste des lectures

        self.menu_contextuel.add_command(label="Supprimer de la liste", command=None)

        self.label_ajouter_lecture = Label(self, text="Vous n'avez enregistré(e) aucune lecture.") # On affiche un texte pour avertir l'utilisateur qu'il n'a enregistré aucune lecture

        self.bouton_ajouter_lecture = Button(self, text="Ajouter une nouvelle lecture...", command=lambda:FenetreAjouter(self, self.raifraichir_liste_lecture)) # On ajoute un bouton pour permettre à l'utilisateur d'ajouter une nouvelle lecture
        
        self.lectures_scrollbar_packed = False # Savoir si la barre de scroll pour la liste des lectures a été intégrée à l'interface graphique ou non
        self.lectures_scrollbar = Scrollbar(self) # Scrollbar pour la liste des lectures
        self.lectures = Listbox(self, yscrollcommand=self.lectures_scrollbar.set) # Listbox contenant toutes les lectures ajoutées par l'utilisateur

        self.lectures_scrollbar.config(command=self.lectures.yview)
        self.lectures_scrollbar.pack(side=RIGHT, fill=Y)
        self.lectures_packed = False # Variable pour savoir si la liste des lectures a été intégrée à l'interface graphique ou non
        self.lectures_enregistrees =  Label(self, text="Vos lectures (cliquez pour ouvrir dans l'éditeur):")
        self.config(menu = self.barre_menus) # On configure le menu de la fenêtre comme étant la barre de menus qu'on a créée

        self.bind("<Control-n>", lambda event:FenetreAjouter(self, self.raifraichir_liste_lecture)) # L'utilisateur peut ajouter une nouvelle lecture avec Ctrl + N
        self.bind("<Control-o>", lambda event:self.ouvrir_lecture(from_list=False)) # L'utilisateur peut ouvrir une lecture avec Ctrl + O
        self.bind("<Control-r>", self.raifraichir_liste_lecture) # L'utilisateur peut rafraîchir la liste de lectures avec Ctrl + R

        self.bind("<Control-q>", self.quitter)

        self.bind("<F1>", lambda event:Editeur(self)) # L'utilisateur peut ouvrir un nouvel éditeur avec F1
        self.bind("<F5>", self.raifraichir_liste_lecture) # L'utilisateur peut également rafraîchir la liste de lectures avec F5

        

        if os.path.exists("paths"): # Si le dossier paths existe
            if os.listdir("paths") == []: # Si le dossier paths est vide, alors on considère qu'aucune lecture n'a été enregistrée
                self.label_ajouter_lecture.pack(fill="both")
                self.bouton_ajouter_lecture.pack()


            else:
                
                self.lectures_enregistrees.pack(fill="both")
                self.lectures.pack(fill="both")
                for fichier in os.listdir("paths"): # Pour chaque fichier du dossier paths
                    print(fichier)
                    if fichier.startswith("chemin_"): # Si le nom du fichier commence par "chemin_"
                       f = open(f"paths/{fichier}", "r") # On veut lire le contenu du fichier
                       contenu_fichier = f.read() # Contenu du fichier
                       chemin_fichier = contenu_fichier + ".json"
                       print(chemin_fichier)
                       titre_livre = os.path.basename(f.read()) # On extrait le titre du livre depuis le chemin contenu dans le fichier texte
                       titre_fichier = fichier[7:] # Titre du livre comme il est contenu dans le fichier
                       titre_livre = titre_fichier
                       titre_livre = titre_livre.replace(".txt", "")
                               
                               

                       print(chemin_fichier)                 
                           
                       if os.path.exists(chemin_fichier): # Si le chemin contenu dans le fichier existe
                            print(f"{chemin_fichier} existe")
                            if not titre_livre in self.lectures.get(0, END):  
                                self.lectures.insert(END, titre_livre)
                            self.titres = [titre for titre in self.lectures.get(0, END)] # On met à jour les titres

                       else:
                           print(f"{chemin_fichier} n'existe pas")     
                       f.close() # On ferme le fichier texte

                
                self.lectures.pack(fill="both", expand=True)
                
                self.lectures_packed = True
                self.lectures_scrollbar_packed = True

                self.lectures.bind("<Double-1>", lambda event: self.ouvrir_lecture(from_list=True, event=event))

                """for entree in self.lectures:
                    entree.bind("<Button-3>", self.afficher_menu_contextuel)"""
                

    def actualiser_menu_favoris(self):
        "Actualiser le menu des favoris"

        """for item in self.menu_favoris.winfo_children(): # Pour chaque item du menu favoris
            if isinstance(item, Menu): # Si l'item est un sous-menu
                continue # On ne détruit pas le sous-menu

            item.destroy()"""
        
        self.menu_favoris.delete(1, "end") # Détruire tous les boutons du menu favoris sauf le premier


        print("Détruit tous les boutons du menu favoris")
        if lister_lectures_favorites() is not [] and self.emplacement_favoris is not None:
                     for dirpath, dirnames, files in os.walk(self.emplacement_favoris): # Pour chaque fichier de lectures
                            
                            fichier_ajoute = False # Savoir le chemin du fichier a été ajouté au menu
                            for file in files: # Pour chaque fichier
                                
                                if file in os.listdir(self.emplacement_favoris): # Si le fichier est à la racine des favoris
                                    chemin = os.path.join(self.emplacement_favoris, file) # Chemin complet vers le fichier                                                          
                                    if not fichier_ajoute:
                                        self.menu_favoris.add_command(label=chemin, command=lambda chemin_lecture=chemin: Editeur(self).ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin)) # Commande pour ouvrir une lecture favorite dans l'éditeur
                                        fichier_ajoute = True

                            for dir in dirnames: # Pour chaque dossier 
                                menu_dossier = Menu(self.menu_favoris, tearoff=0) # Créer un sous-menu pour le dossier
                                chemin = os.path.join(dirpath, dir) # Chemin complet du dossier
                                for element in os.listdir(chemin): # Pour chaque élément du sous-dossier
                                    chemin_lecture = os.path.join(chemin, element) # Chemin complet vers l'élément
                                    if os.path.isfile(chemin_lecture):  # Si l'élément est un fichier
                                            menu_dossier.add_command(label=chemin_lecture, command=lambda chemin_lecture=chemin_lecture: Editeur(self).ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin_lecture))
                                self.menu_favoris.add_cascade(label=dir, menu=menu_dossier)


        self.update_idletasks()  # Mettre à jour la fenêtre             

                

    def demander_creer_favoris(self):
        "Demander à l'utilisateur s'il souhaite créer un dossier de favoris"
        creer = messagebox.askyesno("Créer un dossier de favoris ?", "Cela remplacera tout dossier de favoris créé auparavant") # Demander à l'utilisateur s'il souhaite créer un nouveau dossier de favoris
        if creer == True:     # Si l'utilisateur a confirmé son choix       
            creer_dossier_favoris(choisir_emplacement_favoris()) # Demander à l'utilisateur où il souhaite enregistrer le dossier de favoris

                
    def afficher_menu_contextuel(self, event):
        "Afficher le menu contextuel de la liste des lectures"
        self.menu_contextuel.post(event.x_root, event.y_root) # Afficher le menu contextuel suivant les coordonnées de l'évènement


    def suppr_element_list(event=None):
        "Supprimer un élément de la liste des lectures"
        

    
    def raifraichir_liste_lecture(self, event=None):
        "Rafraîchir l'état de la liste des lectures"
        if not self.lectures_packed: # Si la liste des lectures n'a pas été intégrée à l'interface graphique
            self.lectures.pack(fill="both", expand=True)
            self.lectures.bind("<Double-1>", lambda event: self.ouvrir_lecture(from_list=True, event=event))
            self.lectures_packed = True

        self.label_ajouter_lecture.destroy()
        self.lectures.delete(0, END) # On supprime tous les items de la liste des lectures

        for fichier in os.listdir("paths"): # Remplir la liste des lectures avec les dernières lectures entrées par l'utilisateur
            print(fichier)
            if fichier.startswith("chemin_"): # Si le fichier contient un chemin menant vers une lecture
                with open(f"paths/{fichier}", "r") as f: # On ouvre le fichier en lecture pour trouver le chemin menant vers une lecture
                    contenu_fichier = f.read() # Contenu du fichier
                    print(contenu_fichier)
                    if not contenu_fichier.endswith(".json"):
                        chemin_fichier = contenu_fichier + ".json"

                    else:
                        chemin_fichier = contenu_fichier    
                    titre_livre = os.path.basename(chemin_fichier)
                    
                    if os.path.exists(chemin_fichier):  # Si le chemin existe
                        print(f"{chemin_fichier} existe")  
                        titre_livre = titre_livre.replace(".json", "")
                        if titre_livre not in self.titres:
                            self.lectures.insert(END, titre_livre)
                        self.titres = [titre for titre in self.lectures.get(0, END)]


                    else:
                        print(f"{chemin_fichier} n'existe pas") 

         
                               

    def rechercher_lecture(self, event=None):
        "Rechercher une lecture"
        requete = self.recherche.get() # On obtient la requête de l'utilisateur
        requete_5_cars = requete[:5] # Prendre les 5 premiers caractères de la requête
        print("5 premiers termes de la recherche :", requete_5_cars)
        print(self.titres)


       

        self.lectures.delete(0, END) # On supprime toutes les entrées de la liste des lectures
        for titre in self.titres: # Pour chaque titre de livre
            print("titre :", titre)
            print("titre stripé :", titre.strip())

            if requete == titre.upper() or requete == titre.lower() or requete == titre or titre.startswith(requete_5_cars) : # Si la requête correspond au titre d'un livre
                    if requete == titre.upper() or requete == titre.lower() or requete == titre: # Si la requête est strictement égale au titre
                        self.lectures.delete(0, END) # On retire tous les autres titres qui ne correspondent pas 

                    self.lectures.insert(END, titre) # On insère le résultat dans la liste des lectures
            self.lectures.bind("<Double-1>", lambda event: self.ouvrir_lecture(from_list=True, event=event)) 
          

            
                

        if requete == "":
            self.lectures.delete(0, END)
            for titre in self.titres:
                self.lectures.insert(END, titre)
                self.lectures.bind("<Double-1>", lambda event:self.ouvrir_lecture(from_list=True, event=event))    


    def ouvrir_lecture(self, from_list, event=None):
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
                        Editeur(self).ouvrir_fichier(event=None, dialogue=False, nom_fichier=chemin_fichier) # On ouvre le fichier JSON dans une nouvelle instance de l'éditeur
                        f.close()

        else: # Si l'utilisateur veut ouvrir une lecture depuis un autre endroit que la liste
            Editeur(application_maitre=self).ouvrir_fichier(event=None, dialogue=True) # Créer un nouvel éditeur et ouvrir le fichier dans celui-ci







        
        


    def titre(self, titre):
        "Changer le titre de la fenêtre"
        self.title(titre)


    def quitter(self, event=None):
        "Quitter l'application"
        annuler = False # Variable pour savoir si l'utilisateur a cliqué sur Annuler
        n_editeurs_ouverts = len(editeurs)  # Total des éditeurs ouverts
        editeurs_non_sauv = [] # Liste des éditeurs dont les modifications n'ont pas été sauvegardées
        n_editeurs_non_sauv = len(editeurs_non_sauv) # Total des éditeurs aux modifications non sauvegardées
        for editeur in editeurs: # Pour chaque éditeur ouverts 
            if editeur.winfo_exists():
                if not editeur.modifications_sauvegardees(): # Si les modifications apportées dans l'éditeur n'ont pas été enregistrées
                    editeurs_non_sauv.append(editeur) # On ajoute l'éditeur à la liste des éditeurs non enregistrés
                    n_editeurs_non_sauv = len(editeurs_non_sauv) # On met à jour le nombre d'éditeurs non sauvegardés

        if n_editeurs_non_sauv > 0: # S'il y a des éditeurs non sauvegardés
            enregistrer = messagebox.askyesnocancel("Sauvegarder les modifications ?", f"Il y a {n_editeurs_non_sauv} éditeurs dans lesquel des modifications n'ont pas été enregistrées. Souhaitez-vous enregistrer ces modifications avant de quitter ?") # Demander à l'utilisateur s'il souhaite enregistrer les modifications apportées dans chaque éditeur
            if enregistrer == None: # Si l'utilisateur a cliqué sur Annnuler
                annuler = True
                return 
            
            if enregistrer == True: # Si l'utilisateur veut enregistrer les modifications
                for editeur in editeurs: # Pour chaque éditeur ouvert
                    if editeur.winfo_exists():
                            editeur.enregistrer() # Enregistrer les modifications
                            editeurs_non_sauv.remove(editeur)

                       

            if enregistrer == False: # Si l'utilisateur ne veut pas enregistrer les modifications
                for editeur in editeurs: # Pour chaque éditeur ouvert
                    if editeur in editeurs_non_sauv: # Si l'éditeur contient des modifications non sauvegardées
                        editeurs_non_sauv.remove(editeur)

                    editeur.destroy() # On détruit la fenêtre de l'éditeur
                    editeurs.remove(editeur)

        for editeur in editeurs:
            if editeur.winfo_exists():
                editeur.destroy()
        self.destroy() # Enfin, on détruit la fenêtre d'application principale            




             



app = Application() # On crée une nouvelle instance d'application

app.mainloop() # On exécute la boucle principale
