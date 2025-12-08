import tkinter as tk
from tkinter import filedialog
import shutil
import os

# ----------------------------
# CONFIGURATION DES FICHIERS
# ----------------------------
FILE_VOITURES = "annonces_voitures.csv"
FILE_MOTOS = "annonces_motos.csv"
FILE_LOCATIONS = "annonces_locations.csv"


# ----------------------------
# FONCTION POUR ENREGISTRER UN CSV
# ----------------------------
def telecharger_fichier(fichier_source):
    if not os.path.exists(fichier_source):
        print(f"⚠ Le fichier {fichier_source} est introuvable.")
        return

    destination = filedialog.asksaveasfilename(
        initialfile=fichier_source,
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if destination:
        shutil.copy(fichier_source, destination)
        print(f"✔ Fichier enregistré : {destination}")


# ----------------------------
# INTERFACE TKINTER
# ----------------------------
app = tk.Tk()
app.title("Téléchargement des données Dakar-Auto")
app.geometry("400x300")

label = tk.Label(app, text="Choisissez un fichier à télécharger :", font=("Arial", 14))
label.pack(pady=20)

btn_voitures = tk.Button(
    app,
    text="Télécharger les VOITURES",
    font=("Arial", 12),
    width=30,
    command=lambda: telecharger_fichier(FILE_VOITURES)
)
btn_voitures.pack(pady=5)

btn_motos = tk.Button(
    app,
    text="Télécharger les MOTOS & SCOOTERS",
    font=("Arial", 12),
    width=30,
    command=lambda: telecharger_fichier(FILE_MOTOS)
)
btn_motos.pack(pady=5)

btn_locations = tk.Button(
    app,
    text="Télécharger les LOCATIONS",
    font=("Arial", 12),
    width=30,
    command=lambda: telecharger_fichier(FILE_LOCATIONS)
)
btn_locations.pack(pady=5)

app.mainloop()
