# Sauvegarder une lecture dans un fichier json
from tkinter import filedialog
import json
import os 

def creer_dossier_paths():
    "Créer un dossier dans lequel seront enregistrés les chemins des différents fichiers JSON contenant les lectures"
    os.mkdir("paths") # Le dossier paths contient des fichiers texte dont le contenu indique la localisation des fichiers json

def creer_fichier_chemin(titre,chemin):
    "Créer un fichier contenant le chemin d'un fichier JSON"
    with open(f"paths/chemin_{titre}.txt", "w") as f: # On crée un fichier texte ayant comme nom le titre du livre
        f.write(str(chemin)) # On écrit le chemin menant au fichier JSON
        f.close() # On ferme le fichier



def enregistrer_lecture(titre_livre, annee_livre, auteur_livre, langue_titre, resume_livre):
    "Enregistrer une lecture comme un fichier JSON"
    if not os.path.exists("paths"): # Si le dossier paths n'a pas été créé
        creer_dossier_paths() # Créer le dossier paths, qui contient des fichiers texte dont le contenu est un chemin vers un fichier json

    chemin_fichier = filedialog.asksaveasfilename(title="Où voulez-vous enregistrer votre lecture ?", filetypes=[("Base de données JSON", "*.json")]) # Demander à l'utilisateur où est-ce qu'il veut enregistrer le fichier JSON
    creer_fichier_chemin(titre_livre, chemin_fichier) # Créer un fichier texte contenant le chemin du fichier JSON nouvellement créé


    if not chemin_fichier.endswith(".json"): # Si le fichier n'est pas au format .json
        chemin_fichier += ".json"
    if chemin_fichier:
        donnees_livre = {
            "titre": titre_livre,
            "annee":annee_livre,
            "auteur":auteur_livre,
            "langue":langue_titre,
            "resume":resume_livre
        } # On stocke toutes les données fournies par l'utilisateur concernant le livre

    with open(chemin_fichier, "w") as jsfile: # On écrit dans le fichier JSON nouvellement créé
        json.dump(donnees_livre, jsfile, ensure_ascii=True) # On écrit les données concernant le livre

    