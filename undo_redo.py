"Annuler et refaire des actions"

def undo(champ_texte):
    "Défaire une action"
    champ_texte.edit_undo()  # Défaire la dernière action


def redo(champ_texte):
    "Refaire une action"
    champ_texte.edit_redo()