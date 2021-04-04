import json
from moto import mock_dynamodb2
import boto3


class ProjectsHelper:
    def __init__(self):
        with open('tests/data/projects.json') as json_file:
            self.data = json.load(json_file)
        self.path = "/project"
        self.primary_field = "id"

    def get_invalid_data(self):
        data_copy = self.data
        for item in data_copy:
            item[self.primary_field] = None

        return data_copy

    def get_query_parameters(self, index):
        item = self.data[index]
        return {'id': item['id']}

    @mock_dynamodb2
    def create_table(self):
        mock_dynamodb = boto3.client('dynamodb', 'eu-west-1')

        # Create the DynamoDB table.
        return mock_dynamodb.create_table(
            TableName='project',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )


