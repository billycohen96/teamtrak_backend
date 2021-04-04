import os
"""
ProjectDAO - Handles data access requests related to projects

Parameters:
    db: Object - Object that interacts directly with database.

Methods:
    create(dtos):
    read(ids):
    delete(ids):
"""
from teamtrak_api.data_access_objects.base_dao import BaseDAO
from teamtrak_api.data_transfer_objects.project.project_dto import ProjectDTO


class ProjectDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, table_name=os.environ.get('PROJECT_TN', 'project'), dto=ProjectDTO)

    def process_request(self, http_method, path, dtos, query_parameters) -> dict:
        if http_method == 'POST':
            if path == '/project':
                return self.create(dtos)
            elif path == '/project/add_user':
                return self.add_users_to_project(query_parameters)
            elif path == '/project/remove_user':
                return self.remove_users_from_project(query_parameters)
            elif path == '/project/add_task':
                return self.add_tasks_to_project(query_parameters)
            elif path == '/project/remove_task':
                return self.remove_tasks_from_project(query_parameters)
        elif http_method == 'GET':
            return self.read(query_parameters)
        elif http_method == 'DELETE':
            return self.delete(query_parameters)

    def create(self, dtos: []) -> list:
        # Create project entity
        write_query = []

        # Build query:
        for dto in dtos:
            write_query.append(self.db.upsert_record(dto))

        # Execute query:
        insert_results = self.db.execute_write_transaction(write_query)

        # Add project to creator (user entity)


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
            new_items.append(self.db.convert_dynamodb_record_to_json(item['Item']))

        return new_items

    def add_users_to_project(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            users = [item['users_to_add']]

            query.append(
                self.db.insert_elements_into_ss_attr(key=key, list_attribute='project_users', new_elements=users)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def remove_users_from_project(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            users = [item['users_to_remove']]
            query.append(
                self.db.remove_elements_from_ss_attr(key=key, list_attribute='project_users', remove_elements=users)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def add_tasks_to_project(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            tasks = [item['tasks_to_add']]

            query.append(
                self.db.insert_elements_into_ss_attr(key=key, list_attribute='tasks', new_elements=tasks)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def remove_tasks_from_project(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            tasks = [item['tasks_to_remove']]

            query.append(
                self.db.remove_elements_from_ss_attr(key=key, list_attribute='tasks', remove_elements=tasks)
            )

        result = self.db.execute_write_transaction(query)

        return result
