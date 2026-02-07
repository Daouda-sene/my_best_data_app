import pandas as pd

# =============================
# 1️⃣ DONNÉES DE FATIGUE
# =============================
data_fatigue = pd.DataFrame({
    "Driver": [
        "Amadou", "Fatou", "Mamadou", "Awa", "Cheikh",
        "Mariama", "Ibrahima", "Seynabou", "Ousmane", "Coumba"
    ],
    "Vehicle": [
        "Renault Clio", "Hyundai Tucson", "Toyota Corolla", "Ford Ranger",
        "Peugeot 208", "Kia Picanto", "Mercedes C200", "Volkswagen Golf",
        "Suzuki Vitara", "Nissan Qashqai"
    ],
    "Hours Driving": [2, 5, 3, 8, 6, 4, 7, 2, 9, 1],
    "Fatigue Level (%)": [20, 75, 35, 85, 60, 40, 70, 25, 90, 10]
})

# =============================
# 2️⃣ DONNÉES VÉHICULES
# =============================
data_vehicles = pd.DataFrame({
    "Brand": [
        "Renault Clio 2020", "Hyundai Tucson 2018", "Toyota Corolla 2017",
        "Ford Ranger 2016", "Peugeot 208 2019", "Kia Picanto 2021"
    ],
    "Owner": [
        "Amadou", "Fatou", "Mamadou", "Awa", "Cheikh", "Mariama"
    ],
    "Price (FCFA)": [4500000, 12000000, 8000000, 15000000, 5000000, 3500000],
    "Kilometers": [20000, 50000, 35000, 70000, 15000, 10000],
    "Address": [
        "Dakar", "Pikine", "Guédiawaye", "Mbour", "Rufisque", "Thiès"
    ]
})
import streamlit as st

# ============================
# GESTION DES "ÉCRANS"
# ============================

# Variable de session pour gérer quel écran est affiché
if 'screen' not in st.session_state:
    st.session_state.screen = 'accueil'  # par défaut écran accueil

# ============================
# ÉCRAN ACCUEIL
# ============================
if st.session_state.screen == 'accueil':
    st.title("🚗 SafeDrive App")
    st.write("Bienvenue sur SafeDrive, l'application qui détecte la fatigue du conducteur.")

    st.write("Cliquez sur 'Start Driving' pour démarrer votre trajet.")
    
    if st.button("Start Driving"):
        st.session_state.screen = 'conduite'
        st.experimental_rerun()  # recharge l'app pour afficher l'écran suivant

# ============================
# ÉCRAN CONDUITE
# ============================
elif st.session_state.screen == 'conduite':
    st.title("🛣️ Mode Conduite")
    st.write("Surveillez votre niveau de fatigue pendant le trajet.")

    # Simulation de détection de fatigue
    fatigue = st.slider("Niveau de fatigue du conducteur", 0, 100, 20)

    if fatigue > 70:
        st.warning("⚠️ Niveau de fatigue élevé ! Prenez une pause.")
        if st.button("Alerte Fatigue"):
            st.session_state.screen = 'alerte'
            st.experimental_rerun()

    if st.button("Stop Driving"):
        st.session_state.screen = 'accueil'
        st.experimental_rerun()

# ============================
# ÉCRAN ALERTE
# ============================
elif st.session_state.screen == 'alerte':
    st.title("🚨 Alerte Fatigue !")
    st.write("Vous êtes trop fatigué. Il est recommandé de vous arrêter et de vous reposer.")

    if st.button("OK, je vais faire une pause"):
        st.session_state.screen = 'conduite'
        st.experimental_rerun()

