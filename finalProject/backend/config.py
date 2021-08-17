# backend/config.py

MODEL_PATH = "./models/nowcast/"

models = {
    "MSE": "mse_model",
    "SC": "style_model",
    "MSE+SC": "mse_and_style",
    "cGAN+MAE": "gan_generator",
}