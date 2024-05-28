"check_required vérifie que les dépendances de l'application sont bien installées"
import pkgutil # Importer pkgutil pour installer les modules nécessaires au fonctionnement de l'application
import subprocess

modules_requis = ["newspaper3k", "tkinter", "json", "shutil", "pathlib", "langdetect", "clipboard", "plyer"] # Liste des modules requis pour l'utilisation de l'application

def installer_modules():
    "Installer les modules requis"
    print("Vérification de l'installation des prérequis...")
    for module in modules_requis: # Pour chaque module requis

    
        if pkgutil.find_loader(module) is None: # Si le module n'est pas installé
            
            print(f"Installation des prérequis: {module}...")

            try: # Tenter d'installer le module
                subprocess.check_call(["python", "-m", "pip", "install", module]) # Installer le module

                print(f"Installation de {module} terminée")

            except: # En cas d'erreur lors de l'installation
                print(f"Une erreur s'est produite durant l'installation. L'installation de {module} a été ignorée")
                continue # Tenter d'installer les autres modules nécessaires    
        
        #else:
        #    print(f"{module} est déjà installé")


