import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket=None, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if bucket is None:
        bucket = "com.21n78e.pollyfiles"
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        with open(file_name, "rb") as f:
            response = s3_client.upload_fileobj(f,bucket,object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    s3 = boto3.client('s3')
    file =r"C:\Users\ADMINI~1\AppData\Local\Temp\speech.mp3"
    
    # object_name = 'speech.mp3'
    bucket_name = "com.21n78e.pollyfiles"
    upload_file(file,bucket_name)