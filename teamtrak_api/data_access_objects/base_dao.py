"""
BaseDAO - Handles generic data access requests

Parameters:
    db: object - Object that interacts directly with database.
    table_name: str - Name of table DAO is interacting with.

Methods:
    create(dtos): Takes a list of DTOs, for each DTO build a upsert query, then execute all queries in single transaction
    read(keys): Takes a list of keys (primary key, value) dictionaries, builds a query for each one then executes in single transaction
    delete(keys): Takes a list of keys (primary key, value) dictionaries, builds a query for each one then executes in single transaction
"""
from boto3.dynamodb.types import TypeDeserializer


class BaseDAO:
    def __init__(self, db, table_name, dto):
        self.table_name = table_name
        self.dto = dto
        self.db = db(self.table_name)

    # Creates UserDTOs from msg body
    def create_dtos(self, body: []) -> []:
        dtos = []

        for item in body:
            if isinstance(item, dict):
                dtos.append(self.dto.build(item))

        return dtos

    def process_request(self, http_method, path, dtos, query_parameters) -> dict:
        if http_method == 'POST':
            return self.create(dtos)
        elif http_method == 'GET':
            return self.read(query_parameters)
        elif http_method == 'DELETE':
            return self.delete(query_parameters)

    def create(self, dtos: []) -> list:
        write_query = []

        # Build query:
        for dto in dtos:
            write_query.append(self.db.upsert_record(dto))

        # Execute query:
        insert_results = self.db.execute_write_transaction(write_query)

        # Get ID's from DTOs
        keys = []

        for dto in dtos:
            keys.append({'id': dto.__dict__['id']})

        get_query = []

        for key in keys:
            get_query.append(self.db.read_record(key))

        get_results = self.db.execute_read_transaction(get_query)

        new_items = []

        for item in get_results['Responses']:
            new_items.append(convert_dynamodb_record_to_json(item['Item']))

        return new_items

    def read(self, keys: []) -> list:
        query = []

        # Build query
        for key in keys:
            query.append(self.db.read_record(key))

        # Execute query
        get_results = self.db.execute_read_transaction(query)

        new_items = []
        for item in get_results['Responses']:
            try:
                new_items.append(convert_dynamodb_record_to_json(item['Item']))
            except:
                ''

        return new_items

    def delete(self, keys: []) -> dict:
        query = []

        # Build query
        for key in keys:
            query.append(self.db.delete_record(key))

        # Execute query
        results = self.db.execute_write_transaction(query)

        return results

    def add_elements_to_ss_attr(self, data: [], ss_attr: str, look_for: str, pk_field: str) -> dict:
        query = []

        for item in data:
            # TODO: Error handling - return error message if incorrect fields are provided.
            key = {pk_field: item[pk_field]}
            new_elements = item[look_for]
            query.append(
                self.db.insert_elements_to_ss_attr(key=key, list_attribute=ss_attr, new_elements=new_elements)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def remove_elements_from_ss_attr(self, data: [], ss_attr: str, look_for: str, pk_field: str) -> dict:
        query = []

        for item in data:
            # TODO: Error handling - return error message if incorrect fields are provided.
            key = {pk_field: item[pk_field]}
            remove_elements = item[look_for]
            query.append(
                self.db.remove_elements_from_ss_attr(key=key, list_attribute=ss_attr, remove_elememnts=remove_elements)
            )

        result = self.db.execute_write_transaction(query)

        return result


# Dict in the form:
# {"creation_date": {"S": "2021-02-23 22:32:41.876378"}
# Dict in the form:
# {"creation_date": {"S": "2021-02-23 22:32:41.876378"}
def convert_dynamodb_record_to_json(r, type_deserializer = TypeDeserializer()):
    return type_deserializer.deserialize({"M": r})
