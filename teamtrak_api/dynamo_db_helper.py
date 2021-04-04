import boto3
import json

from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

"""
DynamoDBHelper:
Class used for interfacing with DynamoDB tables, designed to execute queries of a similar nature in
one single transaction - if one operation fails, they all fail.

Uses boto3 library for building DynamoDB (json) dictionaries, these dictionaries are sent to DynamoDB and
represent the actions we want to execute

Parameters:
    table_name: str - name of the table we are interfacing with

Methods:
    read_record(id) -> dict:
        Takes an ID and returns a dictionary for retrieving a record.
    
    delete_record(id) -> dict:
        Takes an ID and returns a dictionary for deleting a record.
    
    upsert_record(dict) -> dict:
        Takes a dictionary of attributes and builds a dictionary for inserting/updating a record.
    
    execute_read_transaction(dict) -> dict:
        Takes a dictionary of a particular format, and uses it to execute a DynamoDB read query, returns results
        
    execute_write_transactions(dict) -> dict:
        Takes a dictionary of a particular format, and uses it to execute a DynamoDB read query, returns results
"""

class DynamoDBHelper:
    table_name: str

    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.client('dynamodb', 'eu-west-1')

    def execute_read_transaction(self, query: list) -> dict:
        result = self.client.transact_get_items(
            TransactItems=query,
            ReturnConsumedCapacity="TOTAL"

        )
        return result

    def execute_write_transaction(self, query: list) -> dict:
        result = self.client.transact_write_items(
            TransactItems=query,
            ReturnConsumedCapacity="TOTAL"
        )
        return result

    def read_record(self, key: dict) -> dict:
        record = self.convert_json_to_dynamodb_record(key)
        return {
            'Get': {
                'TableName': self.table_name,
                'Key': record
            }
        }

    def upsert_record(self, dto) -> dict:
        record = self.convert_json_to_dynamodb_record(dto.get_record())


        return {
            'Put': {
                'TableName': self.table_name,
                'Item': record,
            }
        }

    def delete_record(self, key: dict) -> dict:
        record = self.convert_json_to_dynamodb_record(key)

        return {
            'Delete': {
                'TableName': self.table_name,
                'Key': record,
            }
        }

    # Inserts elements into a specified string set attribute
    def insert_elements_into_ss_attr(self, key: dict, list_attribute: str, new_elements: {}):
        record = self.convert_json_to_dynamodb_record(key)

        return {
            'Update': {
                'TableName': self.table_name,
                'Key': record,
                'UpdateExpression': f'ADD {list_attribute} :element',
                'ExpressionAttributeValues': {':element': {'SS': new_elements}},
            }
        }



    # Removes elements from a specified string set attribute
    def remove_elements_from_ss_attr(self, key: dict, list_attribute: str, remove_elements: []):
        record = self.convert_json_to_dynamodb_record(key)

        return {
            'Update': {
                'TableName': self.table_name,
                'Key': record,
                'UpdateExpression': f'DELETE {list_attribute} :r',
                'ExpressionAttributeValues': {':r': {'SS': remove_elements}}
            }
        }

    def convert_json_to_dynamodb_record(self, r, type_serializer=TypeSerializer()):
        if (isinstance(r, dict)):
            return type_serializer.serialize(r)['M']
        else:
            return type_serializer.serialize(r)

    def convert_dynamodb_record_to_json(self, r, type_deserializer=TypeDeserializer()):
        return type_deserializer.deserialize({"M": r})

