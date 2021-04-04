import json

"""
Class responsible for handling the receiving of events from API Gateway.

Parameters:
    event: dict - Event received to the lambda from API GW. Contains information such as HTTP headers, and which
                    endpoint they are requesting access to

    routing_map: dict - Dictionary that defines which resources to use based on the endpoint.
"""


class APIGatewayEventReceiver:
    def __init__(self, event, routing_map: dict):
        self.event = event
        self.routing_map = routing_map
        # Key values from event
        self.path = self.event['path']

        try:
            self.body = [json.loads(self.event['body'])] if not isinstance(json.loads(self.event['body']), list) else (json.loads(self.event['body']))
        except:
            self.body = []

        self.http_method = (self.event['httpMethod'])
        self.query_parameters = [(self.event['queryStringParameters'])] if not isinstance((self.event['queryStringParameters']), list) else (self.event['queryStringParameters'])

        # Get DTO, DAO and DAO method.
        self.route = self.get_route()
        self.dto = self.route['dto']
        self.dao = self.route['dao']

    def get_route(self) -> dict:
        return self.routing_map[self.path]
