"lignes_vides.py vérifie si une ou plusieurs lignes sont vides après une certaine ligne d'un texte"
#import re


def chaine_vide(texte):
    "Cette fonction indique si le texte donné en paramètre est vide ou non"
    if texte.strip(): # La condition if texte.strip() renvoie True si le texte n'est pas vide
        return False # Le texte n'est pas vide, donc on retourne False
    
    return True # Si le texte est vide, on retourne True

    




def lignes_vides(texte, index_ligne):
    "Vérifier s'il y a des lignes vides après une certaine ligne"
    empty_lines = [] # Liste des lignes vides. Elle est réalisée après qu'une nouvelle ligne non vide soit rencontrée
    lignes = texte.split("\n") # On divise le texte ligne par ligne
    #print("Lignes du texte :", lignes)
    dict_lignes_vides = {} # Dictionnaire qui contient pour valeur chaque ligne non vide et pour chacune de ces lignes non vides le nombre de lignes vides qui suivent
    n_lignes_vides = 0 # Nombre de lignes précédentes après l'actuelle
    #for i, ligne in enumerate(lignes[index_ligne:]): # Itérer sur toutes les lignes après l'index spécifié  

    ligne_actuelle = lignes[index_ligne] # Ligne actuelle
    derniere_ligne_non_vide = None # Dernière ligne non vide
    print("Toutes les lignes après la ligne actuelle :", lignes[index_ligne:])
    for i, ligne in enumerate(lignes[index_ligne:]): # Pour chaque ligne qui suit l'index à partir duquel on doit commencer à compter
        
            if chaine_vide(ligne): # Si la ligne suivante est vide
                 n_lignes_vides += 1 # Incrémenter le compteur de 1
                 if derniere_ligne_non_vide is not None:
                      dict_lignes_vides[derniere_ligne_non_vide] = n_lignes_vides # Mettre à jour le dictionnaire

            else: # Si la ligne suivante n'est pas vide
                 n_lignes_vides = 0 # Remettre le compteur à zéro 
                 derniere_ligne_non_vide = ligne # Mettre à jour la dernière ligne non vide
                 dict_lignes_vides[ligne] = n_lignes_vides # Mettre à jour le dictionnaire         
            
            
            


                 
                  
                
                 




                    


            
            
        
        
        
               

           

        #print(f"Lignes vides après {precedente} : {dict_lignes_vides[precedente]}")
         

        #print("Lignes vides :", dict_lignes_vides)


            
    
    """for i, ligne in enumerate(lignes): # Pour chaque ligne du texte
        print(f"Ligne : '{ligne}'")
        #print(f"Ligne (sans les espaces vides): '{ligne.strip()}'")
        #print(f"Longueur de la ligne : {len(ligne)}")
        #ligne = ligne.replace(" ", "") # Supprimer les espaces dans la ligne
        #print("Ligne (espaces supprimés) :", ligne)
        if i < len(lignes) -1: # Si on est pas à la dernière ligne du texte
            suivante = lignes[i+1].strip() # Ligne suivante par rapport à l'actuelle
            print("Ligne suivante :", suivante)
            if len(suivante) ==0: # Si la ligne suivante est vide
                print(f"La ligne '{suivante}' est vide")
                empty_lines.append(suivante) # Ajouter la ligne à la liste
                print(f"Toutes les lignes vides après {ligne}: {empty_lines}")

            else:
                print(f"La ligne '{suivante}' n'est pas vide")
                        

            if len(ligne) == 0: # Si la ligne actuelle est vide
                print(f"La ligne actuelle ('{ligne}') est vide")
                empty_lines.append(ligne) # Ajouter la ligne actuelle à la liste des lignes vides

            else:
                print(f"La ligne actuelle ('{ligne}') n'est pas vide")"""
   

    return dict_lignes_vides # Retourner le dictionnaire              

    
                        

            
                 

             


"""
texte = '''titre:Ma famille et autres animaux
annee:1957


bebed:cck
resume:Gerald Durell et sa famille, soulés par leur vie à Bornemouth, décident de partir en "exil" à Corfou, grande île de la Grèce. Là-bas, il va se découvrir une grande passion pour la faune et la flore locale.
mon_avis:C'est très bien'''


print(texte)

index_ligne = 2 # Quatrième ligne du texte

empty_lines = lignes_vides(texte, index_ligne) # Lister les lignes vides à partir de la quatrième ligne

print(f"Lignes vides après la ligne {index_ligne + 1}: {empty_lines}")

"""


