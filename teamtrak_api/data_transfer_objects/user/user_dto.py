from dataclasses import dataclass
from teamtrak_api.data_transfer_objects.base_dto import BaseDTO

"""
UserDTO - Represents a user.

BaseDTO Attributes:
    id: primary key
    creation_date: datetime value representing time of data creation

Attributes:
    email_address : email address used by user when logging in
    first_name : 
    last_name :
    member_of : stringified json list containing project_id's that this user is a member ofa
    access_token : personalised git access token for providing teamtrak with access to private git repositories
"""


@dataclass
class UserDTO(BaseDTO):
    email_address: str
    title: str
    first_name: str
    last_name: str
    member_of: set or None
    access_token: str

    def __post_init__(self):
        super(UserDTO, self).__post_init__()

        if not self.member_of:
            self.member_of = None
        else:
            self.member_of = set(self.member_of)

    # Build a ProjectDTO object
    @staticmethod
    def build(record: dict):
        return UserDTO(
            id=record.get('id'),
            email_address=record.get('email_address'),
            title=record.get('title'),
            first_name=record.get('first_name'),
            last_name=record.get('last_name'),
            member_of=record.get('member_of', []),
            access_token=record.get('access_token'),
            creation_date=record.get('creation_date')
        )
