"check_required vérifie que les dépendances de l'application sont bien installées"
import pkgutil # Importer pkgutil pour installer les modules nécessaires au fonctionnement de l'application
import subprocess

modules_requis = ["newspaper3k", "tkinter", "json", "shutil", "pathlib", "langdetect", "clipboard"] # Liste des modules requis pour l'utilisation de l'application

def installer_modules():
    "Installer les modules requis"
    for module in modules_requis: # Pour chaque module requis
        if pkgutil.find_loader(module) is None: # Si le module n'est pas installé
            print(f"Installation de {module}...")
            subprocess.check_call(["python", "-m", "pip", "install", module]) # Installer le module
        else:
            print(f"{module} est déjà installé")


