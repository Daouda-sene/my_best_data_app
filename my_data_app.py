import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Charger le modèle Keras (.h5)
MODEL_PATH = "keras_model.h5"

if not os.path.exists(MODEL_PATH):
    st.error(f"Le fichier {MODEL_PATH} est introuvable ! Assurez-vous qu'il est au même niveau que ce script.")
else:
    model = tf.keras.models.load_model(MODEL_PATH)

    # Labels
    labels = ["fatigue", "non_fatigue"]

    st.title("Détection fatigue chauffeur")

    # Uploader une image
    uploaded_file = st.file_uploader("Uploader une image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Image uploadée", use_column_width=True)

        # Prétraitement pour le modèle
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prédiction
        pred = model.predict(img_array)
        label_index = np.argmax(pred)
        confidence = np.max(pred)

        st.success(f"Résultat : {labels[label_index]} ({confidence*100:.1f}%)")





