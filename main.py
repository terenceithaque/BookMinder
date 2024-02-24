# Script principal
from tkinter import * # Importation de tkinter pour l'interface graphique

class Application(Tk):
    "Classe représentant une instance de l'application. Elle hérite de la classe Tk de tkinter"

    def __ini__(self):
        super().__init__() # On hérite de la classe Tk