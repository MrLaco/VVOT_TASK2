import cv2
import numpy as np

from ymq import Queue
from s3 import S3


def get_faces(image_bytes):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5)

    return faces.tolist()


def handler(event, context):
    queue, s3 = Queue(), S3()

    details = event["messages"][0]["details"]
    bucket = details["bucket_id"]
    object_key = details["object_id"]

    photo = s3.get_object(bucket, object_key)
    faces = get_faces(photo)

    for face in faces:
        queue.send_message({
            "object_key": object_key,
            "face": face,
        })

    return {
        "statusCode": 200,
        "body": None,
    }
