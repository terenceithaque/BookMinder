# Script pour chercher le résumé d'un livre lu
import newspaper # Importation du module newspaper


url = "https://www.wikiwand.com" # URL à partir de laquelle on extraiera le résumé du livre


def titre_en_url(titre):
    "Convertir le titre du livre pour qu'il soit compatible avec une url"
    mots = titre.split() # On découpe le titre du livre mot par mot. Cela nous donne une liste

    titre_converti = "" # Titre sous forme convertie

    for i in range(len(mots)): # Pour toute la longueur de la liste créée par la méthode split() 
        titre_converti += mots[i] # On ajoute le mot correspondant au titre

        if i < len(mots) -1: # Si i est inférieur à longueurs de mots - 1
            titre_converti += "_" # L'URL du à partir de laquelle on extrait le résumé contient un underscore après chaque mot du titre, donc on ajoute un underscore au titre converti après chaque mot sauf le dernier

    return titre_converti


