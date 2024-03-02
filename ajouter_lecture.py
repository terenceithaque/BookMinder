# Script pour ajouter une lecture
from tkinter import * # Importation de tkinter pour l'interface graphique
from tkinter import filedialog # Importation du module filedialog de tkinter pour dialoguer avec les fichiers
from tkinter import messagebox
from resume import * 
from sauvegarder_lecture import *


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

        self.langue_selectionnee = StringVar(self) # Langue du titre sélectionnée par l'utilisateur

        self.langue_selectionnee.set("Anglais (en)")

        options = ["Anglais (en)", "Français (fr)", "Espagnol (es)", "Italien (it)", "Japonais (ja)", "Arabe (ar)", "Estonien (est)"] # Liste des langues que l'utilisateur peut choisir pour le tire du livre
        

        self.label_langue = Label(self, text="Langue du titre du livre :")
        self.label_langue.pack(fill="both")


        self.menu_langue = OptionMenu(self, self.langue_selectionnee, *options) # Menu d'options pour sélectionner la langue du titre
        self.menu_langue.pack()

        self.resume_manuel = False # Variable pour savoir si l'utilisateur souhaite entrer manuellement le résumé du livre


        self.bouton_resume_manuel = Button(self, text="Entrer un résumé du livre manuellement", command=self.ajouter_champ_resume) # Bouton pour permettre à l'utilisateur de saisir son propre résumé du livre

        self.bouton_resume_manuel.pack()

        self.etat_checkbutton_resume_auto = IntVar() # Variable pour stocker l'état du checkbutton créé ci-dessous

        self.etat_checkbutton_resume_auto.trace_add("write", self.champ_resume_auto)
        self.checkbutton_resume_auto = Checkbutton(self, text="Faire un résumé automatiquement", variable=self.etat_checkbutton_resume_auto, command=self.champ_resume_auto) # Bouton pouvant être coché si l'utilisateur veut que le résumé soit fait automatiquement


        self.checkbutton_resume_auto.pack()

        self.champ_resume = Text(self) # Champ de résumé du livre


        self.bouton_enregistrer_lecture = Button(self, text="Enregistrer la lecture...", command=lambda:enregistrer_lecture(self.titre_livre.get(), 
                                                self.annee_livre.get(), self.auteur_livre.get(), self.langue_selectionnee, self.champ_resume.get("1.0", END))) # Bouton pour enregistrer la lecture
        

        self.bouton_enregistrer_lecture.pack()

        


        self.n_champs_resume = 0 # Nombre champs de texte pour le résumé créés par l'utilisateur. S'il est au dessus de 1, on arrête d'en créer.


    def ajouter_champ_resume(self):
        "Faire apparaître un champ de texte pour permettre à l'utilisateur d'entrer un résumé de sa lecture"
        self.resume_manuel = True # On veut écrire un résumé manuellement, donc on passe la variable correspondante sur True
        if self.resume_manuel:
            self.desactiver_bouton(self.checkbutton_resume_auto) # On désactive le bouton de résumé auto

        if self.n_champs_resume < 1: # Si aucun champ de résumé n'a encore été créé
            self.champ_resume.pack(fill="both") 

            self.n_champs_resume += 1


    def champ_resume_auto(self, event=None):
        "Résumé automatique"
        self.resume_auto = True
        if self.resume_auto == True:
            self.desactiver_bouton(self.bouton_resume_manuel) # On désactive le bouton pour le résumé manuel

        if self.etat_checkbutton_resume_auto.get() == 1: # Si le bouton pour le résumé auto est coché
            self.champ_resume.pack(fill="both")

        titre_livre = self.titre_livre.get() # On obtient le titre du livre
        if titre_livre == "": # Si l'utilisateur n'a fourni aucun titre pour le livre
            raise Exception(messagebox.showerror("Aucun titre n'a été fourni", "Vous n'avez fourni aucun titre pour le livre")) # On indique à l'utilisateur qu'il n'a fourni aucun titre

        else: # Si l'utilisateur a fourni un titre
            langues = ["en", "fr", "es", "it", "ja", "ar", "est"] # Codes des différentes langues proposées
            for code in langues:
                if code in self.langue_selectionnee.get():
                    resume = extraire_resume(titre_livre, langue=code) # On obtient le résumé avec le titre du livre et la langue spécifiée par l'utilisateur
                    self.champ_resume.insert("end", resume) # On insère le résumé
                    #self.champ_resume.pack(fill="both")





             


    def desactiver_bouton(self, bouton):
        "Désactiver un bouton"
        bouton.config(state=DISABLED)    



