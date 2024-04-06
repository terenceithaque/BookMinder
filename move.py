"move.py permet de déplacer une lecture d'un endroit à un autre"
import shutil
import os 


def move_file(old_file, new_location):
    "Déplacer un fichier de lecture vers une nouvelle localisation"
    nom_fichier = os.path.basename(old_file) # Nom du du fichier à déplacer
   
    try: 
        shutil.move(old_file, new_location) # Déplacer le fichier
        new_location = os.path.basename(new_location)
        print(f"Déplacé {nom_fichier} vers {new_location}")


    except FileNotFoundError: # Si le fichier à déplacer n'existe pas
        print(f"{nom_fichier} n'existe pas dans {new_location}")   



#move_file("C:\\Données\\Térence\\test4.json", "C:\\Données\\Térence\\Lectures favorites BookMinder")