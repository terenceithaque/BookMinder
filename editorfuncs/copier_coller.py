# Script pour copier un élément dans la mémoire de l'ordinateur
import clipboard
from tkinter import *

def copier(event= None, widget_texte=None):
    "Copier un élément"
    try:
        if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
        

        start_index = widget_texte.index(SEL_FIRST)  # Obtenir la position de début de l'élément à copier dans le widget texte
        stop_index = widget_texte.index(SEL_LAST) # Obtenir la position de fin de l'élément à copier
        texte_a_copier = widget_texte.get(start_index, stop_index)

        if texte_a_copier == "": # Si le texte à copier est vide*
            pass
    
    except TclError:
        return 
    
    
    

    clipboard.copy(texte_a_copier) # Copier l'élément donné en paramètre
    print("Copié ", texte_a_copier)


def couper(event= None, widget_texte=None):
    "Couper un élément"
    try:
        if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
        

        start_index = widget_texte.index(SEL_FIRST)  # Obtenir la position de début de l'élément à copier dans le widget texte
        stop_index = widget_texte.index(SEL_LAST) # Obtenir la position de fin de l'élément à copier
        texte_a_copier = widget_texte.get(start_index, stop_index)

        if texte_a_copier == "": # Si le texte à copier est vide*
            pass
    
    except TclError:
        return 
    
    
    

    clipboard.copy(texte_a_copier) # Copier l'élément donné en paramètre
    widget_texte.delete(start_index, stop_index) # On supprime tout le texte compris entre l'index de début de sélection et l'index de fin de sélection
    print("Coupé ", texte_a_copier)



def coller(event=None,  widget_texte = None):
    "Coller un élément"
    if widget_texte == None: # Si widget_texte est None
            raise Exception(print("wigdet_texte est None")) # On lève une erreur
    

    texte_a_coller = clipboard.paste() # Coller l'élément présent dans le presse-papiers

    widget_texte.insert(INSERT, texte_a_coller) # Insérer le texte à coller à la position actuelle du curseur dans le widget texte

    

