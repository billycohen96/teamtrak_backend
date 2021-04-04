import json
from json import JSONEncoder

"""
This Lambda is responsible for handling HTTP requests related to the retrieval/creation of project information.
"""
# DTO Imports
from teamtrak_api.data_transfer_objects.comment.comment_dto import CommentDTO
from teamtrak_api.data_transfer_objects.project.project_dto import ProjectDTO
from teamtrak_api.data_transfer_objects.task.task_dto import TaskDTO
from teamtrak_api.data_transfer_objects.user.user_dto import UserDTO

# DAO Imports
from teamtrak_api.data_access_objects.comment.comment_dao import CommentDAO
from teamtrak_api.data_access_objects.project.project_dao import ProjectDAO
from teamtrak_api.data_access_objects.task.task_dao import TaskDAO
from teamtrak_api.data_access_objects.user.user_dao import UserDAO

# Other
from teamtrak_api.apigw_receiver import APIGatewayEventReceiver
from teamtrak_api.dynamo_db_helper import DynamoDBHelper

routing_map: dict = {
    '/comment': {'dto': CommentDTO, 'dao': CommentDAO},
    '/comment/upvote': {'dto': CommentDTO, 'dao': CommentDAO},
    '/comment/downvote': {'dto': CommentDTO, 'dao': CommentDAO},
    '/project': {'dto': ProjectDTO, 'dao': ProjectDAO},
    '/project/add_user': {'dto': ProjectDTO, 'dao': ProjectDAO},
    '/project/remove_user': {'dto': ProjectDTO, 'dao': ProjectDAO},
    '/project/add_task': {'dto': ProjectDTO, 'dao': ProjectDAO},
    '/project/remove_task': {'dto': ProjectDTO, 'dao': ProjectDAO},
    '/task': {'dto': TaskDTO, 'dao': TaskDAO},
    '/task/add_user': {'dto': TaskDTO, 'dao': TaskDAO},
    '/task/remove_user': {'dto': TaskDTO, 'dao': TaskDAO},
    '/task/add_comment': {'dto': TaskDTO, 'dao': TaskDAO},
    '/task/remove_comment': {'dto': TaskDTO, 'dao': TaskDAO},
    '/user': {'dto': UserDTO, 'dao': UserDAO},
    '/user/add_project': {'dto': UserDTO, 'dao': UserDAO},
    '/user/remove_project': {'dto': UserDTO, 'dao': UserDAO}
}

def handler(event, context=None):

    api_gw_receiver = APIGatewayEventReceiver(event=event, routing_map=routing_map)
    dao = api_gw_receiver.dao(DynamoDBHelper)
    dtos = dao.create_dtos(api_gw_receiver.body)
    result = dao.process_request(http_method=api_gw_receiver.http_method, path=api_gw_receiver.path, dtos=dtos, query_parameters=api_gw_receiver.query_parameters)
    response_msg = build_response_msg(status_code=200, body=result)

    return response_msg


# Build the required HTTP response message to send back to the client:
def build_response_msg(status_code: int=200, body=""):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, cls=setEncoder),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
    }

class setEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime.datetime):
            return str(obj)

