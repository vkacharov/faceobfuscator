import boto3
import os

class S3Uploader:
    _instance = None
    s3_client = None
    bucket_name = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            echo(f"GETENV {os.getenv("AWS_ACCESS_KEY_ID")} {os.getenv("AWS_SECRET_ACCESS_KEY")} { os.getenv("AWS_DEFAULT_REGION")} { os.getenv('S3_BUCKET_NAME')}" )
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.s3_client = boto3.client(
                "s3",
                aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name = os.getenv("AWS_DEFAULT_REGION")
            )
            cls.bucket_name = os.getenv('S3_BUCKET_NAME')
        return cls._instance
    

    def upload_file(self, prefix, file_name):
        object_name = f"{prefix}/{os.path.basename(file_name)}"
        print(f"Bucket name {self.bucket_name}")
        self.s3_client.upload_file(file_name, self.bucket_name, object_name)
        return object_name
    
    def delete_file(self, object_name):
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
