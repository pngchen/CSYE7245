import sys
sys.path.append('./src/')
import nowcast
import gcsfs
import tensorflow as tf
import h5py
import dataPipeline
import config
import synthetic
import syntheticData

FS = gcsfs.GCSFileSystem(project="Assignment1",
                             token="hardy-portal-318606-3c8e02bd3a5d.json")
# with FS.open(f'gs://assignment1-data/models/nowcast/mse_model.h5', 'rb') as model_file:
#     model_gcs = h5py.File(model_file, 'r')
#     model = tf.keras.models.load_model(model_gcs, compile=False, custom_objects={"tf": tf})
#
# x_test, y_test = dataPipeline.run("SEVIR_VIL_STORMEVENTS_2018_0101_0630", 1)
# name = nowcast.visualize_result(model, x_test, y_test, 0, "MSE")
#
# print(name)

modelName = "MSE_VGG"
idx = 2
model = config.synthetics[modelName]

with FS.open(f'gs://assignment1-data/models/synrad/{model}.h5', 'rb') as model_file:
    model_gcs = h5py.File(model_file, 'r')
    model = tf.keras.models.load_model(model_gcs, compile=False, custom_objects={"tf": tf})

x_test, y_test = syntheticData.get_data(idx)

y_pred = synthetic.run_synrad(model, x_test)

name = synthetic.main(modelName, x_test, y_test, y_pred)

print(name)