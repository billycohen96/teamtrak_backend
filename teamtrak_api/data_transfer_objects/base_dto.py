from dataclasses import dataclass
from datetime import datetime
import json
import uuid

"""
BaseDTO 

Attributes:
    id: primary key
    creation_date: datetime value representing time of data creation

Methods:
    get_json(self):
        Converts DTO into a flat, stringified json object for transfer.
"""


@dataclass
class BaseDTO:
    id: str
    creation_date: str

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

        if self.creation_date is None:
            self.creation_date = str(datetime.utcnow())

    # Converts DTO into a json object, handles datetime objects.
    def get_json(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)

    # Remove all NONE values from dictionary, return record
    def get_record(self):
        record = {}
        for attribute in self.__dict__:
            if self.__dict__[attribute] is not None:
                record[attribute] = self.__dict__[attribute]

        return record
