import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# ==============================
# CONFIG
# ==============================
MODEL_PATH = "keras_model.h5"
LABELS_PATH = "labels.txt"

st.set_page_config(page_title="Fatigue Detection", layout="centered")
st.title("🚗 Détection fatigue chauffeur")

# ==============================
# LOAD MODEL
# ==============================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


# Vérification fichiers
if not os.path.exists(MODEL_PATH):
    st.error("❌ keras_model.h5 introuvable ! Mets-le dans ton repo GitHub.")
    st.stop()

model = load_model()

# ==============================
# LOAD LABELS
# ==============================
if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, "r") as f:
        labels = [line.strip() for line in f.readlines()]
else:
    labels = ["fatigue", "non_fatigue"]

# ==============================
# UPLOAD IMAGE
# ==============================
file = st.file_uploader("📤 Uploader une image", type=["jpg", "png", "jpeg"])

if file:

    img = Image.open(file).convert("RGB")
    st.image(img, caption="Image uploadée", use_column_width=True)

    # ==============================
    # PREPROCESS
    # ==============================
    img = img.resize((224, 224))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # ==============================
    # PREDICTION
    # ==============================
    pred = model.predict(img, verbose=0)

    label_index = np.argmax(pred)
    confidence = float(np.max(pred))

    # ==============================
    # RESULT
    # ==============================
    st.success(
        f"✅ Résultat : **{labels[label_index]}**  |  Confiance : **{confidence*100:.1f}%**"
    )
