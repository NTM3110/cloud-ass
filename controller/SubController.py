import boto3
import config as keys
from boto3.dynamodb.conditions import Key, Attr


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


class SubController:
    def create_table():
        table_name = 'subs'
        existing_tables = client.list_tables()['TableNames']
        if table_name not in existing_tables:
            table = dynamodb.create_table(
                TableName='subs',
                KeySchema=[
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'songTitle',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'songTitle',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName='subs')

    def post_table (title,name):
            
        table = dynamodb.Table('subs')
            
        table.put_item(
            Item={
                'songTitle': title,
                'username': name
            }
        )

    def get_all_item():
            
        table = dynamodb.Table('subs')

        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    
    def delete_item(username, songTitle):
        table = dynamodb.Table('subs')

        table.delete_item(
            Key={
            "username": username,
            "songTitle":songTitle
            }
        )
