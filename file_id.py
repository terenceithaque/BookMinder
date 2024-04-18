"""file_id.py permet de générér un ID permettant de distinguer un fichier de lecture des autres. Cela est utile dans le cas où l'utilisateur
déplace une lecture déjà existante vers les favoris."""
import random # Importer random pour générer des IDs aléatoires
import json # Importer JSON 
import os

try:
    with open("file_ids.json", "r") as f_ids: # Tenter d'ouvrir le fichier des IDs afin de vérifier si des fichiers et leurs IDs ont déjà été enregistrés
        print("Lecture du fichier file_ids.json afin de vérifier les IDs")
        datas = json.load(f_ids) # Charger les données JSON du fichier

        ids = [] # Liste des IDs

        for fichier in datas: # Pour chaque chemin de  fichier contenu dans les données JSON
            if os.path.exists(fichier): # Si le fichier de lecture existe
                print("Le fichier de lecture existe, on ajoute son ID à la liste des IDs")
                id_fichier = datas[fichier] # Obtenir l'ID du fichier
                ids.append(id_fichier) # Ajouter l'ID à la liste
                print("Liste des IDs :", ids)

            else: # Si le fichier n'existe pas
                print(f"L'ID du fichier {fichier} n'a pas été ajouté à la liste car le fichier n'existe pas") 

        f_ids.close() # Fermer le fichier JSON    

except Exception as exc: # En cas d'erreur lors de l'ouverture du fichier file_ids.json
    print("Une erreur s'est produite durant la lecture du fichier file_ids.json :", str(exc)) # Afficher dans la console le message de l'exception
    ids = [] # On initialise la liste des IDs comme étant vide

def generer_id():
    numbers = [i for i in range(101)] # Nombres pouvant être choisis pour l'ID
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
               "j", "k", "l", "m", "n", "o", "p", "q", "r",
               "s", "t","u", "w", "x", "y", "z"] # Lettres pouvant être choisies pour l'ID
    ID = "" # ID du fichier
    id_lenght = 15 # Longueur de l'ID

    while len(ID) < id_lenght: # Tant que la longueur maximale de l'ID n'est pas atteinte
        number = numbers[random.randrange(len(numbers))] # Choisir un nombre au hasard dans la liste des nombres
        ID += str(number) # Ajouter le nombre à l'ID
        letter = letters[random.randrange(len(letters))] # Choisir une lettre au hasard dans la liste des lettres
        ID += letter # Ajouter la lettre à l'ID
    
    while ID in ids: # Si l'ID est a déjà été généré
        print(ID) 
        print(f"Régénération de l'ID {ID} car non unique")
        generer_id() # Générér un nouvel ID


    ids.append(ID) # Ajouter l'ID à la liste
    print("Tous les IDs :", ids)    
    
    return ID # Retourner l'ID

