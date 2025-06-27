import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model once
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("pneumonia_model.h5")

model = load_model()

# Custom styling with updated background color (teal gradient)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #e0f7fa, #b2ebf2);
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #00838f;
        color: white;
        padding: 0.6em 2em;
        border-radius: 9999px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #006064;
    }
    .result-box {
        background-color: #b2ebf2;
        border: 1px solid #4dd0e1;
        padding: 1em;
        border-radius: 1em;
        text-align: center;
        color: #004d40;
        font-weight: 600;
        margin-top: 1.5em;
    }
    .centered-img {
        display: flex;
        justify-content: center;
        margin-bottom: 1em;
    }
    .uploadedFileName, .stFileUploader .uploaded-file-name {
        color: #006064 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .css-1uixxvy.e1b2p2ww15 {
        display: none !important;
    }
    label, footer {
        color: #004d40 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header with X-ray icon
st.markdown("""
    <div class="centered-img">
        <img src="https://img.icons8.com/color/96/lungs.png" width="72" alt="Lungs">
    </div>
    <h1 style='text-align:center; color:#006064;'>Pneumonia Detector</h1>
    <p style='text-align:center; font-size:16px; color:#004d40; font-weight:500;'>
    Upload a chest X-ray image to detect pneumonia using AI
    </p>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Chest X-ray (PNG, JPG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with st.spinner("Analyzing X-ray..."):
        image = Image.open(uploaded_file).convert("RGB")
        resized = image.resize((224, 224))
        input_array = np.array(resized).reshape(1, 224, 224, 3) / 255.0

        # Show uploaded filename
        st.markdown(f"""
            <div style='margin: 0.8em 0 0.3em; font-weight: 600; color: #006064; font-size: 0.95rem;'>
                📄 Uploaded File: {uploaded_file.name}
            </div>
        """, unsafe_allow_html=True)

        # Show image preview
        st.image(image, caption="Uploaded Chest X-ray Image", use_container_width=True)

        # Predict
        prediction = model.predict(input_array)[0][0]

        # Show prediction result
        if prediction > 0.5:
            st.markdown(f"<div class='result-box'>⚠️ <strong>Prediction:</strong> Pneumonia Detected</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-box'>✅ <strong>Prediction:</strong> Normal</div>", unsafe_allow_html=True)

# Footer
st.markdown("<footer style='margin-top: 3em; text-align: center; color: gray;'>This model is for educational demonstration only. It is not validated for clinical use.</footer>", unsafe_allow_html=True)
