"Copier, couper  ou coller du texte depuis ou vers l'éditeur de lecture"

# Script pour copier un élément dans la mémoire de l'ordinateur
import clipboard
from tkinter import *

def copier(event= None, widget_texte=None, all=False):
    "Copier un élément"
    try:
        if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
        
        if all: # S'il faut copier tout le texte contenu dans le champ
            texte_a_copier = widget_texte.get(1.0, END) # Obtenir tout le texte contenu dans le champ
            
        else: # S'il ne faut pas copier l'entièreté du champ de texte
            start_index = widget_texte.index(SEL_FIRST)  # Obtenir la position de début de l'élément à copier dans le widget texte
            stop_index = widget_texte.index(SEL_LAST) # Obtenir la position de fin de l'élément à copier
            texte_a_copier = widget_texte.get(start_index, stop_index)

        if texte_a_copier == "": # Si le texte à copier est vide*
            pass
    
    except TclError:
        return 
    
    
    

    clipboard.copy(texte_a_copier) # Copier l'élément donné en paramètre
    print("Copié ", texte_a_copier)


def couper(event= None, widget_texte=None, all=False):
    "Couper un élément"
    try:
        if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
        
        if all: # S'il faut copier tout le texte du champs
            texte_a_copier = widget_texte.get(1.0, END) # Obtenir tout le texte du champs

        else: # S'il ne faut pas copier tout le champ de texte
            start_index = widget_texte.index(SEL_FIRST)  # Obtenir la position de début de l'élément à copier dans le widget texte
            stop_index = widget_texte.index(SEL_LAST) # Obtenir la position de fin de l'élément à copier
            texte_a_copier = widget_texte.get(start_index, stop_index)

        if texte_a_copier == "": # Si le texte à copier est vide*
            pass
    
    except TclError:
        return 
    
    
    

    clipboard.copy(texte_a_copier) # Copier le texte
    if all:
        widget_texte.delete(1.0, END) # On supprime tout le texte contenu dans le champ

    else:    
        widget_texte.delete(start_index, stop_index)
    print("Coupé ", texte_a_copier)



def coller(event=None,  widget_texte = None):
    "Coller un élément"
    if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
    

    texte_a_coller = clipboard.paste() # Coller l'élément présent dans le presse-papiers
    print("Collé ",texte_a_coller)

    widget_texte.insert(INSERT, texte_a_coller) # Insérer le texte à coller à la position actuelle du curseur dans le widget texte

    

