import boto3
import config as keys
from boto3.dynamodb.conditions import Key, Attr
# Get the service resource.

client = boto3.client('dynamodb',aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name='us-east-1'
                )

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN,
                    region_name='us-east-1')


class MusicController:
    def __init__(self):
        pass

    @staticmethod
    def create_table():
        table_name = 'music'
        
        existing_tables = client.list_tables()['TableNames']
        if table_name not in existing_tables:
            table = dynamodb.create_table(
                TableName='music',
                KeySchema=[
                    {
                        'AttributeName': 'title',
                        'KeyType': 'HASH'
                    }
                    
                ],
                AttributeDefinitions=[
                    {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                    } 
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 200,
                    'WriteCapacityUnits': 200
                }
            )
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='music')

        # Print out some data about the table.
            print(table.item_count)
        return table_name in existing_tables
    
    @staticmethod
    def post_table (title,artist,year,web_url,img_url):
        table = dynamodb.Table('music')
            
        table = dynamodb.Table('music')
        
        table.put_item(
            Item={
                'title': title,
                'artist': artist,
                'year': year,
                'web_url': web_url,
                'img_url': img_url
            }
        )

    def get_all_item():
        table = dynamodb.Table('music')

        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    
    def get_item(title):
        table = dynamodb.Table('music')
        response = table.query(
                KeyConditionExpression=Key('title').eq(title)
        )
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data