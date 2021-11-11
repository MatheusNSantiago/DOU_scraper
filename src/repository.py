import boto3
from .utils import get_env_variable


def upload_to_aws(local_file, bucket, s3_file):

    access_key = get_env_variable("ACCESS_KEY")
    secret_key = get_env_variable("SECRET_KEY")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    s3.upload_file(local_file, bucket, s3_file)
