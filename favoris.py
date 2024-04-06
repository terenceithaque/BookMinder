"Gérer les lectures favorites de l'utilisateur"
import os
from tkinter import filedialog
from plyer import notification
import sys


def chemin_ressource(chemin):
    "Trouver le chemin d'un fichier"
    try:
        base_path = sys._MEIPASS # PyInstaller crée un dossier temp et stocke les chemins dans _MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, chemin)        

def choisir_emplacement_favoris():
    "Choisir un emplacement pour le dossier Lectures favorites"
    global emplacement
    emplacement = filedialog.askdirectory(title="Où enregistrer vos favoris ?") # Demander l'emplacement à l'utilisateur

    return emplacement


def emplacement_favoris():
    "Obtenir l'emplacement du dossier des favoris"
    if os.path.exists("chemin_favoris.txt"):
        f = open("chemin_favoris.txt", "r")
        chemin = f.read()
        f.close()
        return chemin
    else:
        return None


def creer_dossier_favoris(emplacement, icone):
    "Créer un dossier Lectures favorites"
    global emplacement_dossier 
    #try:
    emplacement_dossier = emplacement
    os.makedirs(f"{emplacement_dossier}/Lectures favorites BookMinder") # Créer un dossier Lectures favorites
    icone = chemin_ressource("app_icon.ico")
    notification.notify(title="Le dossier Lectures favorites a été créé avec succès", message=f"Le dossier Lectures favorites ({emplacement_dossier}/Lectures favorites) a été créé avec succès.", app_icon=icone)
    with open("chemin_favoris.txt", "w") as f: # Créer un fichier pour stocker le chemin du dossier des favoris
            print("Emplacement des favoris :", emplacement_dossier + "/" + "Lectures favorites BookMinder")
            f.write(emplacement_dossier + "/" + "Lectures favorites BookMinder")
            f.close()

        
    #except: # En cas d'erreur
        #notification.notify(title="Un problème est survenu", message="Le dossier Lectures favorites n'a pas pû être créé car une erreur s'est produite", app_icon=icone)
def lister_lectures_favorites():
    "Lister toutes les lectures favorites de l'utilisateur"
    emplacement = emplacement_favoris() # Obtenir l'emplacement du dossier des favoris
    if emplacement is not None:
        if os.path.exists(emplacement):
            return os.listdir(emplacement)
    
    return []

    

