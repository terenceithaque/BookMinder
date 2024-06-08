"auto_save.py contient une classe AutoSaveWindow qui permet de configurer l'enregistrement automatique des données"
from tkinter import *
from settings import *
from json import *

settings = read_settings() # Lire le fichier des paramètres

def check_auto_save_enabled():
        "Vérifier si l'enregistrement automatique est activé"
        return settings.get("auto-save-enabled", "false").lower() == "true"

class AutoSaveWindow(Toplevel):
    "Fenêtre pour configurer l'enregistrement automatique"
    def __init__(self, master, text_field, save_func):
        "Constructeur de la fenêtre de configuration de l'enregistrement automatique"
        super().__init__()  # On hérite des attributs de la classe Toplevel

        self.protocol("WM_DELETE_WINDOW", self.terminer) # Enregistrer les paramètres et fermer la fenêtre quand l'utilisateur clique sur le bouton de fermeture
        self.focus_set()
        self.master = master 

        self.master_text_field = text_field # Champ de texte de l'application maître

        self.master_save_func = save_func # Fonction d'enregistrement de l'application maître

        self.key_bindings = {} # Dictionnaire des évènements au clavier et des fonctions qu'ils appellent

        self.title("Configurer l'enregistrement automatique")
        


        self.auto_save = BooleanVar(value = False) # Variable qui permet de déterminer si l'autosave est activé ou non

        if check_auto_save_enabled(): # Si l'enregistrement automatique est activé
            self.auto_save.set(True)
            self.bind_key_release(self.master_text_field, self.master_save_func) # On lie l'enregistrement automatique aux évènements claviers de l'application

        print("Valeur de self.auto_save :", self.auto_save.get())

        self.enable_disable_auto_save()
        self.auto_save_button = Checkbutton(self,text="Enregistrer automatiquement", var=self.auto_save, command=self.enable_disable_auto_save) # Bouton pour activer / désactiver l'enregistrement automatique

        self.auto_save_button.pack()

        self.bouton_terminer = Button(self, text="Terminé", command=self.terminer) # Commande pour fermer la fenêtre de configuration
        self.bouton_terminer.pack()



    def bind_key_release(self, text_field, func):
        "Lier l'évènement KeyRelease à une fonction"
        text_field.bind("<KeyRelease>", func) # Lier l'évènement KeyRelease à la fonction
        self.key_bindings[text_field] = ("<KeyRelease>", func.__name__) # Stocker le nom de la fonction comme une chaîne de caractères


    def unbind_key_release(self, text_field, func):
        "Délier l'évènement KeyRelease d'une fonction"
        key_sequence, func_name = self.key_bindings.get(text_field) # Obtenir la clé de séquence de la fonction et la fonction à délier
        try:
            func_name = str(func_name) # Convertir le nom de la fonction en chaîne de caractères
            print(f"Déliage de {func_name} de {key_sequence}")
            if key_sequence and func_name:
                text_field.unbind(key_sequence, func_name)   
        except Exception as e:
            print(f"Erreur lors du déliage de {func_name} :", e)

    def enable_auto_save(self):
        "Activer l'enregistrement automatique"
        self.auto_save.set(True)
        if not check_auto_save_enabled():
            self.bind_key_release(self.master_text_field, self.master_save_func)
            settings["auto-save-enabled"] = "true" # Mettre ) jour les paramètres
            print("Enregistrement automatique activé")


    def disable_auto_save(self):
        "Désactiver l'enregistrement automatique"
        self.auto_save.set(False)
        if check_auto_save_enabled():
            self.unbind_key_release(self.master_text_field, self.master_save_func)
            settings["auto-save-enabled"] = "false" # Mettre ) jour les paramètres
            print("Enregistrement automatique désactivé")


        

    def enable_disable_auto_save(self):
        "Activer/désactiver l'enregistrement automatique"
        if self.auto_save.get(): # Si l'enregistrement automatique est activé
            #self.auto_save_button.deselect()
            self.enable_auto_save() # Activer l'enregistrement automatique
            
            

        else: # Si l'enregistrement automatique est désactivé
            #self.auto_save_button.select()
            self.disable_auto_save()
            
        
        update_settings(settings)


    def terminer(self):
        "Terminer la configuration et fermer la fenêtre"
        print("Fin de la configuration et fermeture de la fenêtre")
        update_settings(settings) # Mettre à jour les paramètres
        self.destroy() # Quitter la fenêtre    
                


