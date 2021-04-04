import json
from moto import mock_dynamodb2
import boto3

from teamtrak_api.data_transfer_objects.user.user_dto import UserDTO


class UsersHelper:
    def __init__(self):
        with open('tests/data/users.json') as json_file:
            self.data = json.load(json_file)
        self.path = "/user"
        self.primary_field = "email_address"
        self.dto = UserDTO

    def get_invalid_data(self):
        data_copy = self.data
        for item in data_copy:
            item[self.primary_field] = None

        return data_copy

    def get_query_parameters(self, index):
        item = self.data[index]
        return {'email_address': item['email_address']}

    @mock_dynamodb2
    def create_table(self):
        mock_dynamodb = boto3.client('dynamodb', 'eu-west-1')

        # Create the DynamoDB table.
        return mock_dynamodb.create_table(
            TableName='user',
            KeySchema=[
                {
                    'AttributeName': 'email_address',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email_address',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )


