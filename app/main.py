
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from skimage import io
import numpy as np
import time
import tensorflow as tf
import tensorflow_hub as hub
from .gcs import get_cs_file_url


app = FastAPI()

MODEL = tf.keras.models.load_model("./model/model.h5", custom_objects = {"KerasLayer" : hub.KerasLayer})
CLASS_NAMES = ['Healthy', 'Miner', 'Phoma', 'Rust']

class Item(BaseModel):
    url: str
    filename: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/predict")
def predict(item:Item):
    print(item.url)
    print(item.filename)

    link = get_cs_file_url('cs23-ps414-images-bkt', 'item.filename')
    image = io.imread(link)
    image_resize = tf.image.resize(image,[224,224])
    image_batch = np.expand_dims(image_resize,0)

    start_time = time.time()
    prediction = MODEL.predict(image_batch)
    end_time = time.time()

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    inference_time = end_time - start_time
    detected_at = end_time

    return {
        'filename': item.filename,
        'label': predicted_class,
        'confidence': float(confidence),
        'inferenceTime': inference_time,
        'detectedAt': detected_at
    }