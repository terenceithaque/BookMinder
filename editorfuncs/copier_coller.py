# Script pour copier un élément dans la mémoire de l'ordinateur
import clipboard
from tkinter import *

def copier(element, widget_texte):
    "Copier un élément"
    start_index = widget_texte.index(SEL_FIRST)  # Obtenir la position de début de l'élément à copier dans le widget texte
    clipboard.copy(element) # Copier l'élément donné en paramètre


def couper(element, widget_texte):
    "Couper un élément"
    clipboard.copy(element) # Copier l'élément en mémoire

