import base64
import os

import boto3


class S3:
    def __init__(self):
        self.client = boto3.client(
            service_name="s3",
            aws_access_key_id=os.environ["ACCESS_KEY"],
            aws_secret_access_key=os.environ["SECRET_KEY"],
            region_name="ru-central1",
            endpoint_url="https://storage.yandexcloud.net",
        )

    def get_object(self, bucket, object_key) -> bytes:
        response = self.client.get_object(Bucket=bucket, Key=object_key)
        return response["Body"].read()

    def put_object(self, bucket, object_key, body, content_type="binary/octet-stream", metadata=None):
        if metadata:
            metadata = {
                key: base64.b64encode(value.encode("utf-8")).decode("ascii")
                for key, value in metadata.items()
            }

        self.client.put_object(Bucket=bucket, Key=object_key, Body=body, ContentType=content_type, Metadata=metadata)
