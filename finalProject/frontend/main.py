# frontend/main.py

import requests
import streamlit as st
from PIL import Image

models = {
    "MSE": "mse_model",
    "SC": "style_model",
    "MSE+SC": "mse_and_style",
    "cGAN+MAE": "gan_generator",
}

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("nowcast web app")

application = st.selectbox("Choose a application ", ["Synthetic", "Nowcast"])


if application == "Nowcast":
    # displays a file uploader widget
    path = st.text_input('File Path', '')

    idx = st.slider("Choose the Index", 0, 24)

    # displays the select widget for the styles
    model = st.selectbox("Choose the model", [i for i in models.keys()])

    if st.button("Nowcast"):
        if path != '' and model is not None:
            res = requests.post(f"http://backend:8085/{model}/{path}", headers={"Connection": "close"})
            img_path = res.json()
            image = Image.open(img_path.get("name"))
            st.image(image, width=750)

else:
    path = st.text_input('File Path', '')

    if st.button("Synthetic"):
        st.write("Test")