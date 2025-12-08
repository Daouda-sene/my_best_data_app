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

import streamlit as st

# Lecture des fichiers
with open("data/moto_auto.csv", "rb") as f:
    csv1 = f.read()

with open("data/motos.csv", "rb") as f:
    csv2 = f.read()

with open("data/voiture_data.csv", "rb") as f:
    csv3 = f.read()

st.title("Téléchargement des fichiers CSV")

st.download_button(
    label="📄 Télécharger fichier 1",
    data=csv1,
    file_name="fichier1.csv",
    mime="text/csv"
)

st.download_button(
    label="📄 Télécharger fichier 2",
    data=csv2,
    file_name="fichier2.csv",
    mime="text/csv"
)

st.download_button(
    label="📄 Télécharger fichier 3",
    data=csv3,
    file_name="fichier3.csv",
    mime="text/csv"
)




import requests
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------
# 1) CONFIGURATION
# ------------------------------------------------------

KOBOTOOLBOX_TOKEN = "TON_TOKEN_ICI"   # <-- Mets ton token API ici
FORM_ID = "TON_FORM_ID_ICI"           # <-- ID du projet/formulaire
BASE_URL = "https://ee.kobotoolbox.org/x/CtjUrcKt"

headers = {
    "Authorization": f"Token {KOBOTOOLBOX_TOKEN}"
}

# ------------------------------------------------------
# 2) RÉCUPÉRER LES DONNÉES DU FORMULAIRE
# ------------------------------------------------------

url = f"{BASE_URL}/assets/{FORM_ID}/data.json"

response = requests.get(url, headers=headers)

import streamlit as st

if response.status_code != 200:
    st.error("Erreur API KoBoToolbox")
    st.code(response.text)  # affiche la vraie réponse de l’API
    st.stop()

data = response.json()["results"]

# ------------------------------------------------------
# 3) CONVERTIR EN DATAFRAME
# ------------------------------------------------------

df = pd.DataFrame(data)

print("Aperçu des données :")
print(df.head())

# ------------------------------------------------------
# 4) EXEMPLE DE VISUALISATION
#    (ex : distribution des réponses d'une question)
# ------------------------------------------------------

col = "q1"   # mets ici le nom de la question à visualiser

if col in df.columns:
    df[col].value_counts().plot(kind='bar')
    plt.title(f"Distribution de la question : {col}")
    plt.xlabel("Réponse")
    plt.ylabel("Nombre")
    plt.show()
else:
    print(f"⚠️ La question '{col}' n'existe pas dans le dataset.")


