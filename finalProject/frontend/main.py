# frontend/main.py

import gcsfs
import requests
import streamlit as st
from PIL import Image

models = {
    "MSE": "mse_model",
    "SC": "style_model",
    "MSE+SC": "mse_and_style",
    "cGAN+MAE": "gan_generator",
}

synthetics = {
    "GAN_MAE": "gan_mae_weights",
    "MSE_VGG": "mse_vgg_weights",
    "MSE": "mse_weights"
}

FS = gcsfs.GCSFileSystem(project="Assignment1",
                         token="hardy-portal-318606-3c8e02bd3a5d.json")

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Web App")

application = st.selectbox("Choose a application ", ["Synthetic", "Nowcast"])


if application == "Nowcast":
    # displays a file uploader widget
    # path = st.text_input('File Path', '')

    idx = st.slider("Choose the Index", 0, 24)

    # displays the select widget for the styles
    model = st.selectbox("Choose the model", [i for i in models.keys()])

    if st.button("Nowcast"):
        if model is not None:
            res = requests.post(f"http://backend:8085/nowcast/{model}/{idx}", headers={"Connection": "close"})
            img_path = res.json()
            imgRes = FS.open(f'gs://assignment1-data/res/img/{img_path.get("name")}', 'rb')
            image = Image.open(imgRes)
            st.write(img_path.get("name"))
            st.image(image, width=750)

else:
    idx = st.text_input('Index (0 - 235)', '')
    model = st.selectbox("Choose the model", [i for i in synthetics.keys()])

    if st.button("Synthetic"):
        if idx != '' and model is not None:
            res = requests.post(f"http://backend:8085/synthetic/{model}/{idx}", headers={"Connection": "close"})
            img_path = res.json()
            imgRes = FS.open(f'gs://assignment1-data/res/img/{img_path.get("name")}', 'rb')
            image = Image.open(imgRes)
            st.write(img_path.get("name"))
            st.image(image, width=750)