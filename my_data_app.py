import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = "keras_model.h5"

st.title("Détection fatigue chauffeur")

if not os.path.exists(MODEL_PATH):
    st.error("keras_model.h5 introuvable ! Mets-le dans le projet GitHub.")
else:
    model = tf.keras.models.load_model(MODEL_PATH)

    file = st.file_uploader("Uploader une image", type=["jpg", "png", "jpeg"])

    if file:
        img = Image.open(file).convert("RGB")
        st.image(img)

        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img, verbose=0)

        labels = ["fatigue", "non_fatigue"]

        st.success(
            f"Résultat : {labels[np.argmax(pred)]} ({np.max(pred)*100:.1f}%)"
        )
