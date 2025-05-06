# ---------------- imports --------------------
import os
import sys


# -------------- FONCTION QUI RENVOIE LE CHEMIN D'ACCES A UNE RESSOURCE --------------#
# (nécessaire pour les executable car le chemin d'accès devient ...\MEIPASSxxxxx\file.ext)
def resourcePath(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
        print(os.listdir(base_path))
        relative_path = os.path.basename(relative_path)

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)