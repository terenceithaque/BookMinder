"Enregistrer une lecture sur un périphérique de stockage"

# Sauvegarder une lecture dans un fichier json
from tkinter import filedialog
import json
import os 
import file_id

def creer_dossier_paths():
    "Créer un dossier dans lequel seront enregistrés les chemins des différents fichiers JSON contenant les lectures"
    os.mkdir("paths") # Le dossier paths contient des fichiers texte dont le contenu indique la localisation des fichiers json

def creer_fichier_chemin(titre,chemin):
    "Créer un fichier contenant le chemin d'un fichier JSON"
    print("chemin de la lecture à enregister :", chemin)
    with open(f"paths/chemin_{titre}.txt", "w") as f: # On crée un fichier texte ayant comme nom le titre du livre
        chemin.replace("/", "\\")
        f.write(str(chemin)) # On écrit le chemin menant au fichier JSON
        id_fichier = file_id.generer_id() # Générer l'ID du fichier de lecture
        f.write("\n" + id_fichier) # Ecrire l'ID du fichier dans le fichier texte, sur une nouvelle ligne 

        

        f.close() # On ferme le fichier texte 
    
    if not os.path.exists("file_ids.json"): # Si le fichier file_ids.json n'existe pas
         with open("file_ids.json", "w") as ids_file: # Créer le fichier
              ids_file.write(str({})) # Ecrire un dictionnaire vide
              ids_file.close() # Fermer le fichier
         
    with open("file_ids.json", "r+") as jsfile: # Ouvrir le fichier JSON qui contient le chemin et l'ID de chaque fichier

            try:
                 data = json.load(jsfile) # Tenter de charger les données du fichier JSON
                 print("Aucune erreur n'a eue lieu durant la lecture du fichier")

            except json.JSONDecodeError: # En cas de problème lors de la lecture des données
                print("Une erreur s'est produite durant la lecture du fichier")
                data = {} # Initialiser les données du fichier JSON
                jsfile.seek(0) # Déplacer le pointeur du fichier au début du fichier
                jsfile.truncate() # Vider le fichier JSON



        

            data.update({chemin: id_fichier}) # Ajouter le chemin et l'ID du fichier de lecture  au fichier JSON
            jsfile.seek(0) # Déplacer le pointeur du fichier au début du fichier
            json.dump(data, jsfile, indent=4, ensure_ascii=False) # Ecrire les données en JSON
            jsfile.close() # Fermer le fichier JSON

def enregistrer_lecture(titre_livre, annee_livre, auteur_livre, langue_titre, resume_livre, fonction_favoris=None):
    "Enregistrer une lecture comme un fichier JSON"
    if not os.path.exists("paths"): # Si le dossier paths n'a pas été créé
        creer_dossier_paths() # Créer le dossier paths, qui contient des fichiers texte dont le contenu est un chemin vers un fichier json

    chemin_fichier = filedialog.asksaveasfilename(title="Où voulez-vous enregistrer votre lecture ?", filetypes=[("Base de données JSON", "*.json")], defaultextension=".json") # Demander à l'utilisateur où est-ce qu'il veut enregistrer le fichier JSON
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

    with open(chemin_fichier, "w", encoding="utf-8") as jsfile: # On écrit dans le fichier JSON nouvellement créé
        json.dump(donnees_livre, jsfile, ensure_ascii=False) # On écrit les données concernant le livre

    if fonction_favoris is not None: # Si la fonction pour mettre à jour le menu des favoris n'est pas définie comme étant None
            fonction_favoris() # On met à jour le menu des favoris    

    