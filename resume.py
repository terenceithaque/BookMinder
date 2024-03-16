# Script pour chercher le résumé d'un livre lu
import newspaper # Importation du module newspaper
import urllib.parse
from tkinter import messagebox



url = "wikipedia.org/wiki/" # URL à partir de laquelle on extraiera le résumé du livre


def titre_en_url(titre):
    "Convertir le titre du livre pour qu'il soit compatible avec une url"
    mots = titre.split() # On découpe le titre du livre mot par mot. Cela nous donne une liste

    titre_converti = "" # Titre sous forme convertie

    for i in range(len(mots)): # Pour toute la longueur de la liste créée par la méthode split() 
        titre_converti += mots[i] # On ajoute le mot correspondant au titre

        if i < len(mots) -1: # Si i est inférieur à longueurs de mots - 1
            titre_converti += "_" # L'URL du à partir de laquelle on extrait le résumé contient un underscore après chaque mot du titre, donc on ajoute un underscore au titre converti après chaque mot sauf le dernier

    return titre_converti


def extraire_resume(titre, langue):
    "Extraire le résumé d'un livre à partir de son titre"

    try:

        titre = titre.encode("utf-8").decode("utf-8")
        print(titre_en_url(titre))
        url_resume = "https://" + langue + "." + url + titre_en_url(titre)
        url_encodee = urllib.parse.quote(url_resume, safe=":/")
        #print("Url encodée :", url_encodee)
    
        article = newspaper.Article(url_encodee) # On crée un nouvel objet Article à partir de l'URL
        article.download() # On télécharge le contenu HTMl de l'article
        article.parse()

        #print(article.text) # On affiche le résumé du livre

        return article.text
    

    except newspaper.article.ArticleException: # Si une erreur survient lors de l'obtention du résumé
        messagebox.showerror(f"Le livre '{titre}' est introuvable", f"Aucun résultat pour '{titre}'. Il se peut que le titre fourni soit inccorect.")


