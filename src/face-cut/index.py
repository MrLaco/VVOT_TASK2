import io
import json
import os
from uuid import uuid4

from PIL import Image

from s3 import S3


def cut_face(image_bytes, face_coordinates) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    x, y, w, h = face_coordinates

    face = image.crop((x, y, x + w, y + h))
    face_bytes = io.BytesIO()
    face.save(face_bytes, "JPEG")

    return face_bytes.getvalue()


def handler(event, context):
    s3 = S3()

    message = json.loads(event["messages"][0]["details"]["message"]["body"])
    object_key, face_coordinates = message["object_key"], message["face"]

    photo = s3.get_object(os.environ["PHOTOS_BUCKET"], object_key)
    face = cut_face(photo, face_coordinates)

    metadata = {"Original-Photo": object_key}
    s3.put_object(os.environ["FACES_BUCKET"], uuid4().hex + ".jpg", face, "image/jpeg", metadata)

    return {
        "statusCode": 200,
        "body": None,
    }
