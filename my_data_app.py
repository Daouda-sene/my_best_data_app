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








import streamlit as st

st.title("Ouvrir mon Google Form")

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeYZJAwHVc9PaSNHkHdojrK9vyRYfH-tiq76JtFjWBH3GVnJg/viewform?usp=header"

st.markdown(
    f"""
    <a href="{form_url}" target="_blank">
        <button style="
            background-color:#1a73e8;
            color:white;
            padding:10px 20px;
            border:none;
            border-radius:6px;
            font-size:16px;
            cursor:pointer;">
            📄 Ouvrir mon Google Form
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.title("Ouvrir kobotoolbox")

form_url = "https://ee.kobotoolbox.org/x/CtjUrcKt"

st.markdown(
    f"""
    <a href="{form_url}" target="_blank">
        <button style="
            background-color:#1a73e8;
            color:white;
            padding:10px 20px;
            border:none;
            border-radius:6px;
            font-size:16px;
            cursor:pointer;">
            📄 Ouvrir kobotoolbox
        </button>
    </a>
    """,
    unsafe_allow_html=True
)




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ton DataFrame
df = pd.DataFrame({
    "Brand": [
        "Renault Oroch 2021",
        "Bentley Brooklands 2020",
        "Hyundai Santa Fe 2016",
        "Citroen C4 2017",
        "Hyundai Tucson 2018"
    ],
    "Adress": [
        "Nord Foire,Dakar",
        "Dieuppeul Derklé,Dakar",
        "Ouest Foire,Dakar",
        "Sicap Dieuppeul,Dakar",
        "Mbour,Thiès"
    ],
    "Price": [6, 18500000, 5450000, 5700000, 8500],
    "Owner": [
        "Par GABYAUTO GAYE",
        "Par Rose DIOMPY",
        "Par Rose DIOMPY",
        "Par Rose DIOMPY",
        "Par Ibou SARR"
    ]
})

# ============= TITRE DE LA PAGE ==================
st.title("📊 Dashboard Dakar Auto (Data Cleaning + Visualisation)")

# ============= AFFICHAGE DU DATAFRAME ============
st.subheader("📄 Données nettoyées")
st.dataframe(df)

# ============= PLOT 1 : PRIX ================
st.subheader("💰 Prix des véhicules")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df["Brand"], df["Price"])
ax1.set_xticklabels(df["Brand"], rotation=80)
ax1.set_ylabel("Prix (FCFA)")
ax1.set_title("Prix des véhicules")

st.pyplot(fig1)

# ============= PLOT 2 : ANNONCES PAR OWNER ============
st.subheader("👤 Nombre d’annonces par vendeur")

fig2, ax2 = plt.subplots(figsize=(8, 4))
df["Owner"].value_counts().plot(kind="bar", ax=ax2)
ax2.set_title("Nombre d’annonces par propriétaire")
ax2.set_ylabel("Nombre d'annonces")
ax2.set_xticklabels(df["Owner"].value_counts().index, rotation=45)

st.pyplot(fig2)





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Nettoyage des kilomètres
def clean_km(x):
    # Ex: "350 km" → 350
    digits = re.sub(r"[^0-9]", "", str(x))
    return int(digits) if digits else None

# Ton DataFrame (motos)
df = pd.DataFrame({
    "Brand": [
        "SYM 125S 2023",
        "Yamaha TMax 2023",
        "Yamaha X-Max 2025",
        "Honda X-ADV 2021",
        "KTM jakarta 2025"
    ],
    "Adress": [
        "Rufisque,Dakar",
        "VDN,Dakar",
        "Sicap Baobab,Dakar",
        "Cambérène,Dakar",
        "VDN,Dakar"
    ],
    "Price": [620000, 4300000, 800000, 810000, 220000],
    "Owner": [
        "Par Lamine  Ndao",
        "Par Rose  DIOMPY",
        "Par Rose  DIOMPY",
        "Par Rose  DIOMPY",
        "Par Malick konte"
    ],
    "Kilometers": ["1200 km", "1 km", "250 km", "350 km", "6000 km"]
})

# Nettoyer la colonne kilomètres
df["Kilometers"] = df["Kilometers"].apply(clean_km)

# ============= TITRE DE LA PAGE ==================
st.title("🏍️ Dashboard Motos – Dakar Auto")

# ============= AFFICHAGE DU DATAFRAME ============
st.subheader("📄 Données nettoyées des motos")
st.dataframe(df)

# ============= PLOT 1 : PRIX ================
st.subheader("💰 Prix des motos")



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ton DataFrame
df = pd.DataFrame({
    "Brand": [
        "Ford ESCAPE-SE 2013",
        "Ford scape 2013",
        "Ford Edge 2017",
        "Jeep grand-cherokee 2016",
        "Ford Fusion 2014"
    ],
    "Address": [
        "Guédiawaye,Dakar",
        "Guédiawaye,Dakar",
        "Guédiawaye,Dakar",
        "Cambérène,Dakar",
        "Médina,Dakar",
    ],
    "Price": [490000, 490000, 490000, 490000, 490000],
    "Owner": [
        "Par TERANGUA  BII",
        "Par TERANGUA  BII",
        "Par Mouhamed  Sene",
        "Par Mouhamed  Sene",
        "Par Mouhamed  Sene"
    ]
})

# 🔥 AJOUT OBLIGATOIRE
df["Kilometers"] = [120000, 150000, 110000, 180000, 140000]

st.title("Liste des véhicules")
st.dataframe(df, use_container_width=True)

# ========= PLOT 1 ==========
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df["Brand"], df["Price"])
ax1.set_xticklabels(df["Brand"], rotation=80)
ax1.set_ylabel("Prix (FCFA)")
ax1.set_title("Prix des motos")
st.pyplot(fig1)

# ========= PLOT 2 ==========
st.subheader("👤 Nombre d’annonces par vendeur (Owner)")

fig2, ax2 = plt.subplots(figsize=(8, 4))
df["Owner"].value_counts().plot(kind="bar", ax=ax2)
ax2.set_title("Nombre d’annonces par propriétaire")
ax2.set_ylabel("Nombre d'annonces")
ax2.set_xticklabels(df["Owner"].value_counts().index, rotation=45)
st.pyplot(fig2)

# ========= PLOT 3 ==========
st.subheader("🛣️ Kilométrage des motos")

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(df["Brand"], df["Kilometers"])
ax3.set_xticklabels(df["Brand"], rotation=80)
ax3.set_ylabel("Kilométrage (km)")
ax3.set_title("Kilométrage des motos")
st.pyplot(fig3)





