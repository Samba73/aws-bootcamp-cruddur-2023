import boto3
import os, sys
from datetime import datetime, timedelta, timezone
import uuid
import botocore.exceptions

class DDB():
    def client():
        attr = {
            'endpoint_url': 'http://dynamodb-local:8000'
        }

        ddb = boto3.client('dynamodb', **attr)
        return ddb

    def display_message_groups(client, user_uuid):
        tableName = "cruddur-message"
        #print(client)
        #print(user_uuid)
        user_id = user_uuid['uuid']
        #print(user_id)
        partition_key_value = {'S': f"GRP#{user_id}"}
        sort_key_prefix = {'S': str(datetime.now().year)}
        #print(partition_key_value)
        #print('s', sort_key_prefix)
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
        items = response['Items']
        results = []
        datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
        for item in items:
            results.append({
                'uuid': item['message_group_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': item['sk']['S']
            })
        print(results)    
        return results    

    def display_messages(client,message_group_uuid):
        year = str(datetime.now().year)
        table_name = 'cruddur-message'
        query_string = {
        'TableName': table_name,
        'KeyConditionExpression': 'pk = :pkval AND begins_with(sk,:skval)',
        'ScanIndexForward': False,
        'Limit': 20,
        'ExpressionAttributeValues': {
            ':skval': {'S': year },
            ':pkval': {'S': f"MSG#{message_group_uuid}"}
        }
        }

        response = client.query(**query_string)
        items = response['Items']
        items.reverse()
        results = []
        for item in items:
            created_at = item['sk']['S']
            results.append({
                'uuid': item['message_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': created_at
            })
        return results