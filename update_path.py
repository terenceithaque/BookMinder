"update_path.py permet de mettre à jour l'emplacement d'un fichier de lecture"
import json # Impoter le module json 

def update_file_path(container_file, new_path):
    "Mettre à jour le chemin d'un fichier"
    with open(container_file, "w") as f: # Ouvrir le fichier contenant le chemin en écriture
        new_path = str(new_path) # On s'assure que le nouveau chemin est sous forme de chaîne de caractères
        f.write(new_path) # Ecrire le nouveau chemin du fichier 
        f.close() # Fermer le fichier texte contenant le chemin


    
