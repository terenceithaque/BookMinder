# Sauvegarder une lecture dans un fichier json
from tkinter import filedialog
import json
import os 

def creer_dossier_paths():
    "Créer un dossier dans lequel seront enregistrés les chemins des différents fichiers JSON contenant les lectures"
    os.mkdir("paths")


def enregistrer_lecture(titre_livre, annee_livre, auteur_livre, langue_titre, resume_livre):
    "Enregistrer une lecture comme un fichier JSON"
