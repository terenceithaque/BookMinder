"Script pour gérer les paramètres de l'application"
import json # Importer json

settings_file = "settings.json" # Nom du fichier de paramètres


def read_settings():
    "Lire le fichier des paramètres"
    global parametres
    try:
        with open(settings_file, "r") as f: # Ouvrir le fichier de paramètres
            parametres = json.load(f) # Charger les paramètres enregistrés

    except: # En cas d'erreur de lecture du fichier
        parametres = {} # Définir parametres comme un dictionnaire vide

    print("Paramètres :", parametres)
    return parametres


def update_settings(new_settings):
    "Mettre à jour le fichier des paramètres"
    parametres = new_settings 
    with open(settings_file, "w") as f: # Ouvrir le fichier des paramètres
        json.dump(parametres, f, indent=4, sort_keys=True) # Ecrire les paramètres
        f.close() # Fermer le fichier




