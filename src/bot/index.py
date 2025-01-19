import json
import os

from s3 import S3
from telegram import Telegram


def get_face_without_name():
    s3 = S3()

    photos = s3.list_objects(os.environ["FACES_BUCKET"])
    for photo in photos:
        metadata = s3.head_object(os.environ["FACES_BUCKET"], photo)["metadata"]
        if not metadata.get("Name"):
            return photo


def get_face_by_tg_file_unique_id(file_unique_id):
    s3 = S3()

    photos = s3.list_objects(os.environ["FACES_BUCKET"])
    for photo in photos:
        metadata = s3.head_object(os.environ["FACES_BUCKET"], photo)["metadata"]
        if metadata.get("Tg-File-Unique-Id") == file_unique_id:
            return photo


def get_originals_by_name(name):
    s3 = S3()
    originals = []

    photos = s3.list_objects(os.environ["FACES_BUCKET"])
    for photo in photos:
        metadata = s3.head_object(os.environ["FACES_BUCKET"], photo)["metadata"]
        if metadata.get("Name") == name:
            originals.append(metadata["Original-Photo"])

    return originals


def handle_message(message):
    s3, telegram = S3(), Telegram()

    if (text := message.get("text")) and text == "/getface":
        object_key = get_face_without_name()
        if not object_key:
            telegram.send_message("У всех лиц уже заданы имена", message)
            return

        file_unique_id = telegram.send_photo(os.environ["API_GATEWAY_URL"] + f"?face={object_key}", message)
        s3.update_metadata(os.environ["FACES_BUCKET"], object_key, {"Tg-File-Unique-Id": file_unique_id})

    elif (text := message.get("text")) and (reply_message_photo := message.get("reply_to_message", {}).get("photo")):
        file_unique_id = reply_message_photo[-1]["file_unique_id"]
        object_key = get_face_by_tg_file_unique_id(file_unique_id)
        s3.update_metadata(os.environ["FACES_BUCKET"], object_key, {"Name": text})

    elif (text := message.get("text")) and text.startswith("/find"):
        name = text.lstrip("/find ")

        originals = get_originals_by_name(name)
        if not originals:
            telegram.send_message(f"Фотографии с {name} не найдены", message)
            return

        telegram.send_media_group([f"{os.environ["API_GATEWAY_URL"]}/originals/{original}" for original in originals], message)

    else:
        telegram.send_message("Ошибка", message)


def handler(event, context):
    update = json.loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message)

    return {
        "statusCode": 200,
        "body": None,
    }
