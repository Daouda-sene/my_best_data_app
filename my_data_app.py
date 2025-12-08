import streamlit as st
import pandas as pd

# ----------------------------
# TITRE
# ----------------------------
st.title("Téléchargement des données Dakar-Auto")

st.write("Cliquez sur un bouton pour télécharger le fichier correspondant.")

# ----------------------------
# CHARGEMENT DES FICHIERS CSV
# ----------------------------
def load_csv(path):
    try:
        return pd.read_csv(path)
    except:
        st.error(f"⚠ Impossible de charger : {path}")
        return None


df_voitures = load_csv("annonces_voitures.csv")
df_motos = load_csv("annonces_motos.csv")
df_locations = load_csv("annonces_locations.csv")

# ----------------------------
# BOUTONS DE TÉLÉCHARGEMENT
# ----------------------------

if df_voitures is not None:
    st.download_button(
        label="📥 Télécharger les VOITURES",
        data=df_voitures.to_csv(index=False).encode("utf-8"),
        file_name="annonces_voitures.csv",
        mime="text/csv"
    )

if df_motos is not None:
    st.download_button(
        label="📥 Télécharger les MOTOS & SCOOTERS",
        data=df_motos.to_csv(index=False).encode("utf-8"),
        file_name="annonces_motos.csv",
        mime="text/csv"
    )

if df_locations is not None:
    st.download_button(
        label="📥 Télécharger les LOCATIONS",
        data=df_locations.to_csv(index=False).encode("utf-8"),
        file_name="annonces_locations.csv",
        mime="text/csv"
    )

st.success("Interface chargée avec succès !")
