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
