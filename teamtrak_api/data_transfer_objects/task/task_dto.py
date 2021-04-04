from dataclasses import dataclass

from teamtrak_api.data_transfer_objects.base_dto import BaseDTO

"""
Data Transfer Object representing a single task.

Attributes:
    id : unique identifier of task
    name : name of task
    assigned_to_users : stringified json list representing all users who are assigned to this task
    story_point_estimation : integer value representing the length of time to complete task
    epic : boolean representing whether this task is an epic or not
    epic link : link to an epic task.
    complete : boolean representing whether this task is complete or not
    comments: stringified list of json dictionaries representing comments made about task from users.
    created_time : datetime object representing time of project creation
"""


@dataclass
class TaskDTO(BaseDTO):
    name: str
    task_code: str
    description: str
    assigned_to_users: str
    story_point_estimation: str
    epic: bool
    epic_link: str
    comments: set or None
    status: str
    git_branch: str
    epic_due_date: str
    epic_start_date: str
    urgent: bool

    def __post_init__(self):
        super(TaskDTO, self).__post_init__()

        self.story_point_estimation = str(self.story_point_estimation)

        if not self.comments:
            self.comments = None
        else:
            self.comments = set(self.comments)

    # Build a TaskDTO and return
    @staticmethod
    def build(record: dict):
        return TaskDTO(
            id=record.get('id'),
            name=record.get('name'),
            task_code=record.get('task_code'),
            description=record.get('description'),
            assigned_to_users=record.get('assigned_to_users'),
            story_point_estimation=record.get('story_point_estimation'),
            epic_link=record.get('epic_link'),
            epic=record.get('epic'),
            comments=record.get('comments', []),
            creation_date=record.get('creation_date'),
            status=record.get('status'),
            git_branch=record.get('git_branch'),
            epic_due_date=record.get('epic_due_date'),
            epic_start_date=record.get('epic_start_date'),
            urgent=record.get('urgent')
        )
