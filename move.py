"move.py permet de déplacer une lecture d'un endroit à un autre"
import shutil
import os 
import json
import update_path # Importer le module update_path pour mettre à jour le chemin d'un fichier
from pathlib import Path


def move_file(old_file, new_location):
    "Déplacer un fichier de lecture vers une nouvelle localisation"
    ancien_chemin = Path(old_file) # Ancienne localisation du fichier de lecture
    nom_fichier = os.path.basename(old_file) # Nom du du fichier à déplacer
    new_location = Path(new_location)
   
    try: 
        shutil.move(old_file, new_location) # Déplacer le fichier

        
        global id_fichier
        id_fichier = "" # ID du fichier de lecture. C'est pour l'instant une chaîne vide, mais il sera récupéré plus tard
        print("Nouvelle localisation du fichier :", new_location)
        new_location_short = os.path.basename(new_location) # Nouvelle localisation du fichier, raccourcie
        print(f"Déplacé {nom_fichier} vers {new_location_short}")
        nouveau_chemin_complet = Path(os.path.abspath(os.path.join(new_location, nom_fichier))) # Nouveau chemin du fichier, complet
        print("Nouveau chemin du fichier, complet :", nouveau_chemin_complet)
        with open(nouveau_chemin_complet, "r") as f: # Ouvrir le fichier en lecture
            data = json.load(f) # Charger les données JSON du fichier
            f.close()

            titre_lecture = data["titre"] # Extraire le titre de la lecture
            fichier_texte_chemin = Path(os.path.abspath(f"paths/chemin_{titre_lecture}.txt")) # Fichier texte qui contient le chemin vers la lecture
            
            f = open(fichier_texte_chemin, "r") # Ouvrir le fichier texte en lecture
            contenu_fichier_texte = f.readlines() # Lire le contenu du fichier texte
            id_fichier = contenu_fichier_texte[1] if len(contenu_fichier_texte) > 1 else "" # Mettre à jour l'ID du fichier.

            f.close() # Fermer le fichier

            update_path.update_file_path(fichier_texte_chemin, str(nouveau_chemin_complet) +"\n", id_fichier) # Mettre à jour le chemin de la lecture dans le fichier texte et écrire l'ID du fichier

            

    except FileNotFoundError as error: # Si le fichier à déplacer n'existe pas
        print(f"Erreur : {str(error)}")   



#move_file("C:\\Données\\Térence\\test4.json", "C:\\Données\\Térence\\Lectures favorites BookMinder")