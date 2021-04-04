import os
import time
"""
UserDAO - Handles data access requests related to users

Parameters:
    db: Object - Object that interacts directly with database.

Methods:
    create(dtos):
    read(ids):
    delete(ids):
"""
from teamtrak_api.data_access_objects.base_dao import BaseDAO, convert_dynamodb_record_to_json
from teamtrak_api.data_transfer_objects.user.user_dto import UserDTO


class UserDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, table_name=os.environ.get('USER_TN', 'user'), dto=UserDTO)

    def process_request(self, http_method, path, dtos, query_parameters) -> dict:
        if http_method == 'POST':
            if path == '/user':
                return self.create(dtos)
            elif path == '/user/add_project':
                return self.add_projects_to_user(query_parameters)
            elif path == '/user/remove_project':
                return self.remove_projects_from_user(query_parameters)
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
            keys.append({'email_address': dto.__dict__['email_address']})

        get_query = []

        for key in keys:
            get_query.append(self.db.read_record(key))


        get_results = self.db.execute_read_transaction(get_query)


        new_items = []

        for item in get_results['Responses']:
            try:
                new_items.append(convert_dynamodb_record_to_json(item['Item']))
            except:
                ''

        return new_items

    def add_projects_to_user(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'email_address': item['email_address']}
            projects = [item['projects_to_add']]

            query.append(
                self.db.insert_elements_into_ss_attr(key=key, list_attribute='member_of', new_elements=projects)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def remove_projects_from_user(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'email_address': item['email_address']}
            users = [item['projects_to_remove']]

            query.append(
                self.db.remove_elements_from_ss_attr(key=key, list_attribute='member_of', remove_elements=users)
            )

        result = self.db.execute_write_transaction(query)

        return result
