from dataclasses import dataclass
from datetime import datetime
from teamtrak_api.data_transfer_objects.base_dto import BaseDTO
import json

"""
Data Transfer Object representing a single project.

Attributes:
    id: unique identifier of project
    name: name of project
    creator: single id representing the id of the user that created the project
    tasks: string set representing the id's of all tasks that have been assigned to project
    users: string set representing the id's of all users who have access to the project
    creation_date: datetime object representing time of project creation
"""


@dataclass
class ProjectDTO(BaseDTO):
    name: str
    description: str
    creator: str
    tasks: set or None
    project_users: set or None
    git_repo: str
    project_code: str

    def __post_init__(self):
        super(ProjectDTO, self).__post_init__()

        if not self.tasks:
            self.tasks = None
        else:
            self.tasks = set(self.tasks)

        if not self.project_users:
            self.project_users = None
        else:
            self.project_users = set(self.project_users)

        if not isinstance(self.project_users, set):
            raise ValueError

    # Build a ProjectDTO and return
    @staticmethod
    def build(record: dict):
        return ProjectDTO(
            id=record.get('id'),
            name=record.get('name'),
            description=record.get('description'),
            creator=record.get('creator'),
            tasks=record.get('tasks', []),
            project_users=record.get('project_users', []),
            creation_date=record.get('creation_date'),
            git_repo=record.get('git_repo'),
            project_code=record.get('project_code')
        )
