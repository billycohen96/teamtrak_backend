import os
"""
CommentDAO - Handles data access requests related to comments

Parameters:
    db: Object - Object that interacts directly with database.

Methods:
    create(dtos):
    read(ids):
    delete(ids):
"""
from teamtrak_api.data_access_objects.base_dao import BaseDAO
from teamtrak_api.data_transfer_objects.comment.comment_dto import CommentDTO


class CommentDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, table_name=os.environ.get('COMMENT_TN', 'comment'), dto=CommentDTO)

    def process_request(self, http_method, path, dtos, query_parameters) -> dict:
        if http_method == 'POST':
            return self.create(dtos)
        elif http_method == 'GET':
            return self.read(query_parameters)
        elif http_method == 'DELETE':
            return self.delete(query_parameters)
