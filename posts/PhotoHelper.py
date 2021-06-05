from google.cloud import storage
import uuid
import os

storage_client = storage.Client()
media_bucket = storage_client.get_bucket(os.environ["MEDIA_BUCKET"])

def upload_photo(photo):
    blob = media_bucket.blob(f'{uuid.uuid4()}')
    blob.upload_from_file(photo, content_type="image/jpeg")
    blob.make_public()
    return blob.public_url