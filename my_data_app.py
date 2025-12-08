import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import unicodedata

# ======================================================
# FUNCTION : CLEAN PRICE
# ======================================================
def clean_price(raw):
    """Nettoie un prix comme '3 500 000 FCFA' → 3500000."""
    if not raw:
        return None
    raw = unicodedata.normalize("NFKC", raw)
    raw = raw.replace("FCFA", "").replace("CFA", "")
    digits = re.sub(r"[^0-9]", "", raw)
    if digits == "":
        return None
    return int(digits)


# ======================================================
# SCRAPER GENERIC
# ======================================================
def scrape(url, mode):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    soup = bs(res.content, "html.parser")
    cards = soup.find_all("div", class_="listing-card__content p-2")

    data = []

    for card in cards:
        try:
            # URL annonce
            a = card.find("a")
            annonce_url = "https://dakar-auto.com" + a["href"] if a else None

            # Brand
            brand_tag = card.find("h2", class_="listing-card__header__title mb-md-2 mb-0")
            brand = brand_tag.get_text(strip=True) if brand_tag else "Introuvable"

            # Adresse
            adress_tag = card.find("div", class_="col-12 entry-zone-address")
            adress = adress_tag.get_text(strip=True) if adress_tag else "Introuvable"

            # Prix
            price_tag = card.find("h3", class_="listing-card__header__price font-weight-bold text-uppercase mb-0")
            if price_tag:
                price = clean_price(price_tag.get_text(strip=True))
            else:
                price = None

            # Owner
            owner_tag = card.find("p", class_="time-author m-0")
            owner = owner_tag.get_text(strip=True) if owner_tag else "Inconnu"

            # Détails (motos only)
            details_blocks = card.find_all("div", class_="col-12 listing-card__properties d-none d-sm-block")
            details = []
            for blk in details_blocks:
                for li in blk.find_all("li"):
                    details.append(li.get_text(strip=True))

            km = details[1] if len(details) > 1 else None

            dic = {
                "Brand": brand,
                "Address": adress,
                "Price": price,
                "Owner": owner,
                "Kilometers": km,
                "URL": annonce_url
            }

            data.append(dic)

        except Exception:
            continue

    return pd.DataFrame(data)


# ======================================================
# SCRAPING URLs
# ======================================================
URL_VOITURES = "https://dakar-auto.com/senegal/voitures-4"
URL_MOTOS = "https://dakar-auto.com/senegal/motos-and-scooters-3"
URL_LOCATIONS = "https://dakar-auto.com/senegal/location-de-voitures-19"


# ======================================================
# STREAMLIT UI
# ======================================================
st.title("🚗📊 Dakar-Auto Scraper App")
st.write("Scraping : voitures • motos • location")

choice = st.selectbox(
    "Sélectionnez une catégorie",
    ["Voitures", "Motos", "Location de voitures"]
)

if st.button("Scraper maintenant"):
    with st.spinner("Scraping en cours..."):

        if choice == "Voitures":
            df = scrape(URL_VOITURES, mode="cars")

        elif choice == "Motos":
            df = scrape(URL_MOTOS, mode="motos")

        else:
            df = scrape(URL_LOCATIONS, mode="rent")

    st.success(f"{len(df)} annonces trouvées !")
    st.dataframe(df)

    # Téléchargement CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name=f"{choice.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import platform

# Fonction pour ouvrir un fichier selon le système
def open_file(path):
    if not os.path.exists(path):
        messagebox.showerror("Erreur", f"Le fichier n'existe pas : {path}")
        return

    system = platform.system()

    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":  # macOS
            subprocess.call(["open", path])
        else:  # Linux
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Chemins vers tes fichiers
file1 = "data/fichier1.csv"
file2 = "data/fichier2.csv"
file3 = "data/fichier3.csv"

# Interface Tkinter
root = tk.Tk()
root.title("Ouvrir mes fichiers CSV")
root.geometry("300x200")

btn1 = tk.Button(root, text="Ouvrir fichier 1", command=lambda: open_file(file1), width=25)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Ouvrir fichier 2", command=lambda: open_file(file2), width=25)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Ouvrir fichier 3", command=lambda: open_file(file3), width=25)
btn3.pack(pady=10)

root.mainloop()



