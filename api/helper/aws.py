import boto3
from boto3.s3.transfer import S3Transfer

from .config import IC_AWS_ACCESS_KEY_ID, IC_AWS_DEFAULT_REGION, IC_S3_BUCKET, IC_AWS_SECRET_ACCESS_KEY

def upload_file(absolute_file_location):
    file_name = absolute_file_location.split('/')[-1]
    credentials = { 
        'aws_access_key_id': IC_AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': IC_AWS_SECRET_ACCESS_KEY
    }

    s3_client = boto3.client('s3', IC_AWS_DEFAULT_REGION, **credentials)
    transfer = S3Transfer(s3_client)

    transfer.upload_file(
        absolute_file_location, 
        IC_S3_BUCKET, 
        file_name,
        extra_args={
            'ACL': 'public-read',
            'ContentType': 'image/png'
        }
    )

    file_url = '%s/%s/%s' % (s3_client.meta.endpoint_url, IC_S3_BUCKET, file_name)
    return file_url