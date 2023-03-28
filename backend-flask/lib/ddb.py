import boto3
import os, sys
from datetime import datetime, timedelta, timezone
import uuid

class DDB():
    def client():
        attr = {
            'endpoint_url': 'http://localhost:8000'
        }
        if len(sys.argv) == 2:
            if "prod" in sys.argv[1]:
                attr = {}

        ddb = boto3.client('dynamodb', **attr)
        return ddb

    def display_message_groups(client, user_uuid):
        tableName = "cruddur-message"


        query_string = {
            'TableName': tableName,
            'ScanIndexForward': False,
            'ReturnConsumedCapacity': 'TOTAL',
            'Limit': 20,
            'KeyConditionExpression': 'pk = :pkval AND begins_with(sk, :skval)',
        #    'KeyConditionExpression': 'pk = :pkval AND sk BETWEEN :sk1 AND :sk2 ',
            'ExpressionAttributeValues':{
                ':pkval': partition_key_value,
                ':skval': sort_key_prefix
        #        ':sk1': {'S': '2023-03-01T08:59:04.737763+00:00'},
        #        ':sk2': {'S': '2023-03-26T08:59:04.737763+00:00'},
            }
        }
        response = client.query(**query_string)
        return response