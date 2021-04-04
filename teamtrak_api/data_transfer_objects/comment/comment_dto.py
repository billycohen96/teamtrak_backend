from dataclasses import dataclass
from datetime import datetime

from teamtrak_api.data_transfer_objects.base_dto import BaseDTO

"""
Data Transfer Object representing a single comment.

Comments are found under tasks. Any user can make a comment on any task. 

Attributes:
    id : unique identifier
    user : id representing the user who made the comment
    content : content of comment, string.
    creation_date : datetime object representing time of comment creation
    
"""


@dataclass
class CommentDTO(BaseDTO):
    user: str
    content: str

    def __post_init__(self):
        super(CommentDTO, self).__post_init__()

    # Build a CommentDTO and return
    @staticmethod
    def build(record: dict):
        return CommentDTO(
            id=record.get('id'),
            user=record.get('user'),
            content=record.get('content'),
            creation_date=record.get('creation_date')
        )
