"Remplacer un caractère ou un texte entier par un autre"

# Script pour rechercher et remplacer du texte
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import re




def afficher_dialogue_remplacer(fenetre_maitre):
    "Afficher un dialogue pour remplacer un texte"
    global fenetreRemplacer
    fenetreRemplacer = Toplevel(fenetre_maitre) # On crée une fenêtre pour demander à l'utilisateur quel texte il faut remplacer

    avertissement = Label(fenetreRemplacer, text="Cette opération remplacera toutes les occurences d'un texte donné.") # Avertissement à l'utilisateur quant à ce que fera cette action
    avertissement.config(bg="red")
    avertissement.pack()
    label_texte_a_remplacer = Label(fenetreRemplacer, text="Remplacer :") # Label pour demander à l'utilisateur quel texte remplacer
    label_texte_a_remplacer.pack(fill="both")
    entree_remplacer = Entry(fenetreRemplacer) # Entrée pour saisir le texte à remplacer
    entree_remplacer.pack(fill="both")

    label_texte_remplacement = Label(fenetreRemplacer, text="par :") # Label pour demander à l'utilisateur quel texte mettre à la place de l'ancien
    label_texte_remplacement.pack(fill="both")

    entree_nouveau_texte = Entry(fenetreRemplacer) # Entrée pour saisir le nouveau texte
    entree_nouveau_texte.pack(fill="both")

    bouton_remplacer = Button(fenetreRemplacer, text="Remplacer toutes les occurences...", command=lambda:remplacer(fenetre_maitre.champ_texte, entree_remplacer.get(), entree_nouveau_texte.get())) # Bouton pour remplacer toutes les occurences d'un texte
    bouton_remplacer.pack(fill="both")

    fenetreRemplacer.mainloop()


def remplacer(widget_texte, texte_a_remplacer, nouveau_texte):
    "Remplacer un texte par un nouveau"
    texte = widget_texte.get(1.0, END) # Extraire le texte contenu dans le widget Texte
    occurences = texte.count(texte_a_remplacer) # Compter toutes les occurences du texte à remplacer
    if occurences == 0: # S'il n'y a aucune occurence dans le widget Texte
        messagebox.showinfo("Aucune occurence trouvée", f"Aucune occurence n'a été trouvée pour {texte_a_remplacer}.") # Afficher un message pour indiquer à l'utilisateur qu'aucune occurence n'a été trouvée
        fenetreRemplacer.destroy()
        return # On appelle le mot-clé return afin d'arrêter le travail de remplacement directement
    
    else: # Si des occurences ont été trouvées 
        texte = texte.replace(texte_a_remplacer, nouveau_texte) # On remplace l'ancien texte par le nouveau
        widget_texte.delete(1.0, END) # On supprime tout l'ancien texte du widget Texte
        widget_texte.insert(1.0, texte) # On ajoute le texte mis à jour dans le widget texte
        
    fenetreRemplacer.destroy()


        


