import inference
import gcsfs
import tensorflow as tf
import h5py
import dataPipeline

FS = gcsfs.GCSFileSystem(project="Assignment1",
                             token="hardy-portal-318606-3c8e02bd3a5d.json")
with FS.open(f'gs://assignment1-data/models/nowcast/mse_model.h5', 'rb') as model_file:
    model_gcs = h5py.File(model_file, 'r')
    model = tf.keras.models.load_model(model_gcs, compile=False, custom_objects={"tf": tf})

x_test, y_test = dataPipeline.run("SEVIR_VIL_STORMEVENTS_2018_0101_0630", 1)
name, modelName = inference.visualize_result(model, x_test, y_test, 0, "MSE")

print(name)