from datetime import datetime, timedelta
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'app/gcs-sa-key.json'

def get_cs_file_url(bucket_name, file_name, expire_in=datetime.today() + timedelta(1)): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url