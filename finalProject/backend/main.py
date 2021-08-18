# backend/main.py

import uuid

import cv2
import sys
sys.path.append('./src/')
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import UploadFile
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import gcsfs
import tensorflow as tf
import h5py

from readers.nowcast_reader import read_data
import config
import nowcast
import synthetic
import dataPipeline
import syntheticData


app = FastAPI()

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.get("/")
def read_root():
    return {"message": "Welcome from the nowcast API"}

@app.post("/synthetic/{modelName}/{idx}")
async def get_synthetic(modelName: str, idx: int):
    FS = gcsfs.GCSFileSystem(project="Assignment1",
                             token="hardy-portal-318606-3c8e02bd3a5d.json")
    model = config.synthetics[modelName]

    with FS.open(f'gs://assignment1-data/models/synrad/{model}.h5', 'rb') as model_file:
        model_gcs = h5py.File(model_file, 'r')
        model = tf.keras.models.load_model(model_gcs, compile=False, custom_objects={"tf": tf})
        model = 3

    # x_test, y_test = syntheticData.get_data(idx)
    #
    # y_pred = synthetic.run_synrad(model, x_test)
    #
    # name = synthetic.main(modelName, x_test, y_test, y_pred)

    return {"name": model}

@app.post("/nowcast/{modelName}/{datapath}")
async def get_nowcast(modelName: str, datapath: str):
    FS = gcsfs.GCSFileSystem(project="Assignment1",
                             token="hardy-portal-318606-3c8e02bd3a5d.json")
    model = config.models[modelName]

    with FS.open(f'gs://assignment1-data/models/nowcast/{model}.h5', 'rb') as model_file:
        model_gcs = h5py.File(model_file, 'r')
        model = tf.keras.models.load_model(model_gcs, compile=False, custom_objects={"tf": tf})

    x_test, y_test = dataPipeline.run(datapath, 1)

    name = nowcast.visualize_result(model, x_test, y_test, 0, modelName)

    return {"name": name}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085)