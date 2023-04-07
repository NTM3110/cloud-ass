import logging
import json
import boto3
from botocore.exceptions import ClientError
import config as keys
import urllib.request
from controller.MusicController import MusicController

s3_client = boto3.client('s3', aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name='us-east-1'
                )

class S3Controller:

    @staticmethod
    def create_bucket(bucket_name, region=None):
        try:
            if region is None:
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
    
    def show_image(bucket):
        musics_set = {}
        try:
            for item in s3_client.list_objects(Bucket=bucket)['Contents']:
                presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
                # public_urls.append(presigned_url)
                # print(presigned_url)
                # print(item['Key'])
                musics_set[item['Key']] = presigned_url
                print("\n")

        except Exception as e:
            pass
        # print(json.dumps(musics_set, indent=4))
        print(musics_set.get("#40.jpg"))
        return musics_set
    

    def download_image(bucket):
        musics = MusicController.get_all_item()
        for music in musics:
            s3_client.download_file(bucket, f"{music['title']}.jpg", f"../image/{music['title']}.jpg")
