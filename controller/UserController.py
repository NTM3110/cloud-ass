import boto3
import config as keys
from boto3.dynamodb.conditions import Key, Attr
# Get the service resource.


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN)


class UserController:
    def create_table():
        table = dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                }
                
            ],
            AttributeDefinitions=[
                {
                'AttributeName': 'email',
                'AttributeType': 'S'
                } 
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='userdata')

    # Print out some data about the table.
        print(table.item_count)


    def post_table (name,email,password):
        table = dynamodb.Table('login0')
            
        table = dynamodb.Table('login0')
            
        table.put_item(
            Item={
                'username': name,
                'email': email,
                'password': password
            }
        )

    @classmethod
    def check(email):
        table = dynamodb.Table('login')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        return response['Items']
