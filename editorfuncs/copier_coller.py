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


def couper(element, widget_texte):
    "Couper un élément"
    clipboard.copy(element) # Copier l'élément en mémoire

