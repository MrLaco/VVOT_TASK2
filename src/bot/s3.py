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

    def get_object(self, bucket, object_key):
        response = self.client.get_object(Bucket=bucket, Key=object_key)
        return {
            "body": response["Body"].read(),
            "metadata": response["Metadata"],
        }

    def put_object(self, bucket, object_key, body, metadata=None):
        if metadata:
            metadata = {
                key: base64.b64encode(value.encode("utf-8")).decode("ascii")
                for key, value in metadata.items()
            }

        self.client.put_object(Bucket=bucket, Key=object_key, Body=body, Metadata=metadata)

    def list_objects(self, bucket):
        response = self.client.list_objects(Bucket=bucket)
        return map(lambda obj: obj["Key"], response.get("Contents", []))

    def head_object(self, bucket, object_key):
        response = self.client.head_object(Bucket=bucket, Key=object_key)
        return {"metadata": {
                key: base64.b64decode(value).decode("utf-8")
                for key, value in response["Metadata"].items()
        }}

    def update_metadata(self, bucket, object_key, metadata):
        old_metadata = self.head_object(bucket, object_key)["metadata"]
        new_metadata = {**old_metadata, **metadata}

        new_metadata = {
            key: base64.b64encode(value.encode("utf-8")).decode("ascii")
            for key, value in new_metadata.items()
        }

        self.client.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": object_key},
            Key=object_key,
            Metadata=new_metadata,
            MetadataDirective="REPLACE",
        )
