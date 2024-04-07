"file_id.py permet de générér un ID permettant de distinguer un fichier de lecture des autres"
import random

ids = [] # Liste des IDs

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
        generer_id() # Générér un nouvel ID
    
    return ID # Retourner l'ID

