
from fastapi import FastAPI
from io import BytesIO
from PIL import Image
from pydantic import BaseModel
import numpy as np
import requests
import time
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing.image import img_to_array


app = FastAPI()

MODEL = tf.keras.models.load_model("./model/model.h5", custom_objects = {"KerasLayer" : hub.KerasLayer})
CLASS_NAMES = ['Healthy', 'Miner', 'Phoma', 'Rust']

class Item(BaseModel):
    url: str
    filename: str

def transform_image(img):
    img = img_to_array(img)
    img = img.astype(np.float64) / 255
    imgs = tf.image.resize(img, [224,224])
    imgs = np.expand_dims(imgs, axis=0)
    return imgs

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/predict")
def predict(item:Item):
    response = requests.get(item.url)
    image = Image.open(BytesIO(response.content))
    image = transform_image(image)

    start_time = time.time()
    prediction = MODEL.predict(image)
    end_time = time.time()

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    inference_time = (end_time - start_time)  * 10**(-3)

    return {
        'filename': item.filename,
        'label': predicted_class,
        'confidence': float(confidence),
        'inferenceTime': inference_time,
        'detectedAt': end_time
    }