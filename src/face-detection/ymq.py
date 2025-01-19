import json
import os

import boto3


class Queue:
    def __init__(self):
        self.client = boto3.client(
            service_name="sqs",
            endpoint_url="https://message-queue.api.cloud.yandex.net",
            region_name="ru-central1",
            aws_access_key_id=os.environ["ACCESS_KEY"],
            aws_secret_access_key=os.environ["SECRET_KEY"],
        )

    def send_message(self, message):
        self.client.send_message(QueueUrl=os.environ["QUEUE_URL"], MessageBody=json.dumps(message))
