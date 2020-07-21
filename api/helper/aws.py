import boto3
from boto3.s3.transfer import S3Transfer

from .config import IC_AWS_ACCESS_KEY_ID, IC_AWS_DEFAULT_REGION, IC_S3_BUCKET, IC_AWS_SECRET_ACCESS_KEY

AWS_CREDENTIALS = {
    'aws_access_key_id': IC_AWS_ACCESS_KEY_ID,
    'aws_secret_access_key': IC_AWS_SECRET_ACCESS_KEY,
    'region_name': IC_AWS_DEFAULT_REGION
}

def upload_file(file_byte, file_name):
    """ Uploads a BytesIO object from memory to the AWS S3 Bucket and returns the file url """
    s3 = boto3.resource('s3', **AWS_CREDENTIALS)
    s3.Object(IC_S3_BUCKET, file_name).put(Body = file_byte.getvalue(), ContentType = 'image/png', ACL = 'public-read')
    file_url = 'https://{}.s3.{}.amazonaws.com/{}'.format(IC_S3_BUCKET, IC_AWS_DEFAULT_REGION, file_name)
    return file_url