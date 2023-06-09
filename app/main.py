from fastapi import FastAPI
from io import BytesIO
from PIL import Image
from pydantic import BaseModel
import base64
import logging
import numpy as np
import requests
import time
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing.image import img_to_array
import configparser
from fastapi.responses import JSONResponse

app = FastAPI()

MODEL = tf.keras.models.load_model("./model/model.h5", custom_objects = {"KerasLayer" : hub.KerasLayer})
CLASS_NAMES = ['Healthy', 'Miner', 'Phoma', 'Rust']

class MessageReq(BaseModel):
    message: dict
    subscription: str

def transform_image(img):
    img = img_to_array(img)
    img = img.astype(np.float64) / 255
    imgs = tf.image.resize(img, [224,224])
    imgs = np.expand_dims(imgs, axis=0)
    return imgs

def get_url_image_service():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get("credentials", "image-service")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(req: MessageReq):
    try:
        envelope = req.message
        logging.warning(req.message)
        logging.warning('Message Masuk')

        payload = base64.b64decode(envelope['data'])
        payload = payload.decode()
        payload = eval(payload)

        response = requests.get(payload['url'])
        image = Image.open(BytesIO(response.content))
        image = transform_image(image)

        start_time = time.time() * 1000
        prediction = MODEL.predict(image)
        end_time = time.time() * 1000

        predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
        confidence = np.max(prediction[0])
        inference_time = end_time - start_time

        data = {
            'filename': payload['filename'],
            'label': predicted_class,
            'confidence': float(confidence),
            'inferenceTime': round(inference_time),
            'detectedAt': round(end_time)
        }

        response = {
            "message": "Success",
            "data": data
        }
        status_code = 200

    except ValueError as e:
        logging.warning(req.message)
        logging.warning(e.__str__())
        data = None
        response = {
            "message": e.__str__(),
            "data": data
        }
        status_code = 400

    except Exception as e:
        logging.warning(req.message)
        logging.warning(e.__str__())
        data = None
        response = {
            "message": e.__str__(),
            "data": data
        }
        status_code = 500

    image_service = get_url_image_service()
    requests.put(image_service + 'image-detections/update', data=data)

    return JSONResponse(content=response, status_code=status_code)
