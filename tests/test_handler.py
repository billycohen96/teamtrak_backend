import os, sys, json, unittest
from moto import mock_dynamodb2
from decimal import *
import boto3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.helpers.comments_helper import CommentsHelper
from tests.helpers.projects_helper import ProjectsHelper
from tests.helpers.tasks_helper import TasksHelper
from tests.helpers.users_helpers import UsersHelper

from teamtrak_api import lambda_function

from teamtrak_api.data_access_objects import *
from teamtrak_api.data_transfer_objects import *
from teamtrak_api.dynamo_db_helper import *

class TestHandlerCase(unittest.TestCase):
    @mock_dynamodb2
    # Test POST, GET, DELETE and PUT operations via valid message bodies and queries parameters.
    def test_valid_crud_operations(self):
        helpers = [UsersHelper(), TasksHelper(), ProjectsHelper(), CommentsHelper()]

        for helper in helpers:
            # Create table:
            helper.create_table()

            for i in range(0, 10):
                # Insert Record
                post_event = create_apigw_event(path=helper.path, http_method='POST', body=helper.data[i],
                                                query_params=None)
                lambda_function.handler(event=post_event, context=None)

                # Get record
                query_parameters = helper.get_query_parameters(i)
                get_event = create_apigw_event(path=helper.path, http_method='GET', body=None,
                                               query_params=query_parameters)
                response = lambda_function.handler(event=(get_event), context=None)

                # Check if record is inserted:
                self.assertEqual(json.loads(response['body'])[0][helper.primary_field],
                                 helper.data[i][helper.primary_field])

                # Delete record
                delete_event = create_apigw_event(path=helper.path, http_method='DELETE', body=None,
                                                  query_params=query_parameters)
                lambda_function.handler(event=(delete_event), context=None)

                # Get record
                query_parameters = helper.get_query_parameters(i)
                get_event = create_apigw_event(path=helper.path, http_method='GET', body=None,
                                               query_params=query_parameters)
                response = lambda_function.handler(event=(get_event), context=None)

                # Check if record is deleted
                self.assertEqual(json.loads(response['body']), [])

    @mock_dynamodb2
    def test_adding_user_to_project(self):
        users_helper = UsersHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        users_helper.create_table()
        projects_helper.create_table()

        # Insert user and project
        user = users_helper.data[4]
        project = projects_helper.data[0]

        # Project creation event
        create_project_event = create_apigw_event(path=projects_helper.path, http_method='POST',
                                                  body=project,
                                                  query_params=None)
        # Send event to API
        lambda_function.handler(event=create_project_event, context=None)

        # Insert the user to the projects user set event
        add_users_to_project_event = create_apigw_event(path='/project/add_user', http_method='POST', body=None,
                                                        query_params={'id': project['id'],
                                                                      'users_to_add': user['email_address']})

        # Send event to API
        lambda_function.handler(event=add_users_to_project_event, context=None)

        # Get project record
        get_event = create_apigw_event(path='/project', http_method='GET', body=None,
                                       query_params={'id': project['id']})

        # Check result
        response = lambda_function.handler(event=(get_event), context=None)

        self.assertTrue(user['email_address'] in json.loads(response['body'])[0]['project_users'])

    @mock_dynamodb2
    def test_removing_user_from_project(self):
        users_helper = UsersHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        users_helper.create_table()
        projects_helper.create_table()

        # Insert user and project
        user = users_helper.data[0]
        project = projects_helper.data[0]

        # Project creation event
        create_project_event = create_apigw_event(path=projects_helper.path, http_method='POST',
                                                  body=project,
                                                  query_params=None)
        # Send event to API
        lambda_function.handler(event=create_project_event, context=None)

        # Insert the user to the projects user set event
        remove_users_from_project_event = create_apigw_event(path='/project/remove_user', http_method='POST', body=None,
                                                        query_params={'id': project['id'],
                                                                      'users_to_remove': user['email_address']})

        # Send event to API
        lambda_function.handler(event=remove_users_from_project_event, context=None)

        # Get project record
        get_event = create_apigw_event(path='/project', http_method='GET', body=None,
                                       query_params={'id': project['id']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)

        self.assertTrue(user['email_address'] not in json.loads(response['body'])[0]['project_users'])

    @mock_dynamodb2
    def test_adding_task_to_project(self):
        tasks_helper = TasksHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        projects_helper.create_table()

        # Insert user and project
        task = tasks_helper.data[8]
        project = projects_helper.data[0]

        # Project creation event
        create_project_event = create_apigw_event(path=projects_helper.path, http_method='POST',
                                                  body=project,
                                                  query_params=None)
        # Send event to API
        lambda_function.handler(event=create_project_event, context=None)

        # Insert the user to the projects user set event
        add_task_to_project_event = create_apigw_event(path='/project/add_task', http_method='POST', body=None,
                                                             query_params={'id': project['id'],
                                                                           'tasks_to_add': task['id']})

        # Send event to API
        lambda_function.handler(event=add_task_to_project_event, context=None)

        # Get project record
        get_event = create_apigw_event(path='/project', http_method='GET', body=None,
                                       query_params={'id': project['id']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)

        self.assertTrue(task['id'] in json.loads(response['body'])[0]['tasks'])

    @mock_dynamodb2
    def test_removing_task_from_project(self):
        tasks_helper = TasksHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        projects_helper.create_table()

        # Insert user and project
        task = tasks_helper.data[0]
        project = projects_helper.data[0]

        # Project creation event
        create_project_event = create_apigw_event(path=projects_helper.path, http_method='POST',
                                                  body=project,
                                                  query_params=None)
        # Send event to API
        lambda_function.handler(event=create_project_event, context=None)

        # Insert the user to the projects user set event
        remove_task_from_project_event = create_apigw_event(path='/project/remove_task', http_method='POST', body=None,
                                                       query_params={'id': project['id'],
                                                                     'tasks_to_remove': task['id']})

        # Send event to API
        lambda_function.handler(event=remove_task_from_project_event, context=None)

        # Get project record
        get_event = create_apigw_event(path='/project', http_method='GET', body=None,
                                       query_params={'id': project['id']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)

        self.assertTrue(task['id'] not in json.loads(response['body'])[0]['tasks'])

    @mock_dynamodb2
    # Test retrieval of a list of projects belonging to a particular user
    def test_adding_project_to_user(self):
        users_helper = UsersHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        users_helper.create_table()

        # Insert user and project
        user = users_helper.data[0]
        project = projects_helper.data[1]

        # Project creation event
        create_user_event = create_apigw_event(path=users_helper.path, http_method='POST',
                                                  body=user,
                                                  query_params=None)


        # Send event to API
        lambda_function.handler(event=create_user_event, context=None)

        # Insert the user to the projects user set event
        add_project_to_user_event = create_apigw_event(path='/user/add_project', http_method='POST', body=None,
                                                            query_params={'email_address': user['email_address'],
                                                                          'projects_to_add': project['id']})

        # Send event to API
        lambda_function.handler(event=add_project_to_user_event, context=None)

        # Get project record
        get_event = create_apigw_event(path='/user', http_method='GET', body=None,
                                       query_params={'email_address': user['email_address']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)

        self.assertTrue(project['id'] in json.loads(response['body'])[0]['member_of'])

    @mock_dynamodb2
    # Test retrieval of a list of projects belonging to a particular user
    def test_removing_project_from_user(self):
        users_helper = UsersHelper()
        projects_helper = ProjectsHelper()

        # Create user and project tables:
        users_helper.create_table()

        # Insert user and project
        user = users_helper.data[0]
        project = projects_helper.data[0]

        # Project creation event
        create_user_event = create_apigw_event(path=users_helper.path, http_method='POST',
                                               body=user,
                                               query_params=None)


        # Send event to API
        lambda_function.handler(event=create_user_event, context=None)

        # Insert the user to the projects user set event
        remove_project_from_user = create_apigw_event(path='/user/remove_project', http_method='POST', body=None,
                                                       query_params={'email_address': user['email_address'],
                                                                     'projects_to_remove': project['id']})

        # Send event to API
        lambda_function.handler(event=remove_project_from_user, context=None)

        # Get project record
        get_event = create_apigw_event(path='/user', http_method='GET', body=None,
                                       query_params={'email_address': user['email_address']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)


        self.assertTrue(json.loads(response['body'])[0].get('member_of') is None)


    @mock_dynamodb2
    # Test retrieval of a list of projects belonging to a particular user
    def test_adding_comment_to_task(self):
        tasks_helper = TasksHelper()
        comments_helper = CommentsHelper()

        # Create user and project tables:
        tasks_helper.create_table()

        # Insert user and project
        task = tasks_helper.data[0]
        comment = comments_helper.data[0]

        # Project creation event
        create_user_event = create_apigw_event(path=tasks_helper.path, http_method='POST',
                                               body=task,
                                               query_params=None)


        # Send event to API
        lambda_function.handler(event=create_user_event, context=None)

        # Insert the user to the projects user set event
        add_comment_to_task = create_apigw_event(path='/task/add_comment', http_method='POST', body=None,
                                                      query_params={'id': task['id'],
                                                                    'comments_to_add': comment['id']})

        # Send event to API
        lambda_function.handler(event=add_comment_to_task, context=None)

        # Get project record
        get_event = create_apigw_event(path='/task', http_method='GET', body=None,
                                       query_params={'id': task['id']})

        # Check result
        response = lambda_function.handler(event=get_event, context=None)

        self.assertTrue(comment['id'] in json.loads(response['body'])[0]['comments'])

    # Test building DTOs from msg bodies:
    def test_dto_creation(self):
        helpers = [UsersHelper(), ProjectsHelper(), CommentsHelper(), TasksHelper()]

        for helper in helpers:
            dto = helper.dto.build(helper.data[0])

            self.assertEqual(type(dto), helper.dto)

        self.assertTrue(True)

    # Test the building of a create query within the DynamoDBHelper class
    def test_create_query_building(self):
        db = DynamoDBHelper(table_name='test')

        dto = UsersHelper().dto.build(UsersHelper().data[0])

        self.assertTrue(db.upsert_record(dto=dto), {'Put': {'TableName': 'test', 'Item': {'id': {'S': 'b3ef12cd-16f5-4c31-b282-f77f7178a639'}, 'creation_date': {'S': '2021-04-04 14:59:18.159274'}, 'email_address': {'S': 'bob_khan2@kcl.ac.uk'}, 'first_name': {'S': 'bob'}, 'last_name': {'S': 'khan'}, 'member_of': {'SS': ['938197cf-eee5-40b7-9e4e-af21b241a7d1']}}}})

    # Test the building of a read query within the DynamoDBHelper class
    def test_read_query_building(self):
        db = DynamoDBHelper(table_name='test')

        self.assertEqual(db.read_record(key={'email_address': 'test123@test123.com'}), {'Get': {'TableName': 'test', 'Key': {'email_address': {'S': 'test123@test123.com'}}}})

    # Test the conversion of JSON into DynamoDB JSON
    def test_json_to_dynamodb_json_conversion(self):
        db = DynamoDBHelper(table_name='test')

        self.assertEqual(db.convert_json_to_dynamodb_record('s'), {'S': 's'})
        self.assertEqual(db.convert_json_to_dynamodb_record(3), {'N': '3'})
        self.assertEqual(db.convert_json_to_dynamodb_record({'a'}), {'SS': ['a']})

    # Test the conversion of DynamoDB JSON into JSON
    def test_dynamodb_json_to_json_conversion(self):
        db = DynamoDBHelper(table_name='test')

        self.assertEqual(db.convert_dynamodb_record_to_json({'M': {'S': 's'}}), {'M': 's'})
        self.assertEqual(db.convert_dynamodb_record_to_json({'M': {'N': '3'}}), {'M': Decimal('3')})
        self.assertEqual(db.convert_dynamodb_record_to_json({'M': {'SS': ['a']}}), {'M': {'a'}})



def create_apigw_event(path, http_method, body, query_params):
    return {
        "body": json.dumps(body),
        "resource": "/{proxy+}",
        "path": path,
        "httpMethod": http_method,
        "isBase64Encoded": "true",
        "queryStringParameters": query_params,
        "multiValueQueryStringParameters": {
            "foo": [
                "bar"
            ]
        },
        "pathParameters": {
            "proxy": "/path/to/resource"
        },
        "stageVariables": {
            "baz": "qux"
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.eu-west-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": [
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ],
            "Accept-Encoding": [
                "gzip, deflate, sdch"
            ],
            "Accept-Language": [
                "en-US,en;q=0.8"
            ],
            "Cache-Control": [
                "max-age=0"
            ],
            "CloudFront-Forwarded-Proto": [
                "https"
            ],
            "CloudFront-Is-Desktop-Viewer": [
                "true"
            ],
            "CloudFront-Is-Mobile-Viewer": [
                "false"
            ],
            "CloudFront-Is-SmartTV-Viewer": [
                "false"
            ],
            "CloudFront-Is-Tablet-Viewer": [
                "false"
            ],
            "CloudFront-Viewer-Country": [
                "US"
            ],
            "Host": [
                "0123456789.execute-api.eu-west-1.amazonaws.com"
            ],
            "Upgrade-Insecure-Requests": [
                "1"
            ],
            "User-Agent": [
                "Custom User Agent String"
            ],
            "Via": [
                "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
            ],
            "X-Amz-Cf-Id": [
                "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
            ],
            "X-Forwarded-For": [
                "127.0.0.1, 127.0.0.2"
            ],
            "X-Forwarded-Port": [
                "443"
            ],
            "X-Forwarded-Proto": [
                "https"
            ]
        },
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "requestTime": "09/Apr/2015:12:34:56 +0000",
            "requestTimeEpoch": 1428582896000,
            "identity": {
                "cognitoIdentityPoolId": "null",
                "accountId": "null",
                "cognitoIdentityId": "null",
                "caller": "null",
                "accessKey": "null",
                "sourceIp": "127.0.0.1",
                "cognitoAuthenticationType": "null",
                "cognitoAuthenticationProvider": "null",
                "userArn": "null",
                "userAgent": "Custom User Agent String",
                "user": "null"
            },
            "path": "/prod/path/to/resource",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "apiId": "1234567890",
            "protocol": "HTTP/1.1"
        }
    }


if __name__ == '__main__':
    unittest.main()
