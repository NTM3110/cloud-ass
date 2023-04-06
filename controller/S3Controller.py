import logging
import boto3
from botocore.exceptions import ClientError
import config as keys
import urllib.request



class S3Controller:

    @staticmethod
    def create_bucket(bucket_name, region=None):
        try:
            if region is None:
                s3_client = boto3.client('s3', aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name=region
                )
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name=region
                )
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)

        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    def upload_file(file_url, bucket, object_name):
# If S3 object_name was not specified, use file_name
        s3_client = boto3.client('s3', aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name='us-east-1'
                )
        try:
            link = file_url
            f = urllib.request.urlopen(link)
            myfile = f.read()
            response = s3_client.put_object(
                Bucket = "song-image",
                Body = myfile,
                Key=object_name+".jpg",
            )
        except ClientError as e:
            logging.error(e)
            return False
        return True