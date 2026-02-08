import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = "saved_model"   # dossier

if not os.path.exists(MODEL_PATH):
    st.error("Le dossier saved_model est introuvable !")
else:
    model = tf.keras.models.load_model(MODEL_PATH)

    labels = ["fatigue", "non_fatigue"]

    st.title("Détection fatigue chauffeur")
    pred = model.predict(img, verbose=0)


    uploaded_file = st.file_uploader("Uploader une image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Image uploadée", use_column_width=True)

        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)

        label_index = np.argmax(pred)
        confidence = np.max(pred)

        st.success(f"Résultat : {labels[label_index]} ({confidence*100:.1f}%)")

