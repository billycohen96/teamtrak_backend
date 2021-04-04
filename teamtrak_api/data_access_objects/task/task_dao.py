import os

"""
TaskDAO - Handles data access requests related to tasks

Parameters:
    db: Object - Object that interacts directly with database.

Methods:
    create(dtos):
    read(ids):
    delete(ids):
"""
from teamtrak_api.data_access_objects.base_dao import BaseDAO
from teamtrak_api.data_transfer_objects.task.task_dto import TaskDTO


class TaskDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, table_name=os.environ.get('TASK_TN', 'task'), dto=TaskDTO)

    def process_request(self, http_method, path, dtos, query_parameters) -> dict:
        if http_method == 'POST':
            if path == '/task':
                return self.create(dtos)
            elif path == '/task/add_comment':
                return self.add_comments_to_task(query_parameters)
            elif path == '/remove_comments_from_task':
                return self.remove_comments_from_task(query_parameters)
        elif http_method == 'GET':
            return self.read(query_parameters)
        elif http_method == 'DELETE':
            return self.delete(query_parameters)

    def add_comments_to_task(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            comments = [item['comments_to_add']]

            query.append(
                self.db.insert_elements_into_ss_attr(key=key, list_attribute='comments', new_elements=comments)
            )

        result = self.db.execute_write_transaction(query)

        return result

    def remove_comments_from_task(self, data: []) -> dict:
        query = []

        for item in data:
            key = {'id': item['id']}
            comments = item['comments_to_remove']

            query.append(
                self.db.remove_elements_from_ss_attr(key=key, list_attribute='assigned_to_users',
                                                     remove_elements=comments)
            )

        result = self.db.execute_write_transaction(query)

        return result
