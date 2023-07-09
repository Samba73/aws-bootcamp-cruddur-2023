import boto3
import os, sys
from datetime import datetime, timedelta, timezone
import uuid
import botocore.exceptions

class DDB():
    def client():
        attr = {
            'endpoint_url': os.getenv("AWS_ENDPOINT_URL")
        }

        ddb = boto3.client('dynamodb', **attr)
        return ddb
    
    def display_message_groups(client, tableName, user_uuid):
        table_name = tableName
        #print(client)
        print(user_uuid)
        user_id = user_uuid
        #print(user_id)
        partition_key_value = {'S': f"GRP#{user_id}"}
        sort_key_prefix = {'S': str(datetime.now().year)}
        #print(partition_key_value)
        #print('s', sort_key_prefix)
        query_string = {
            'TableName': table_name,
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
                'message_group_uuid': item['message_group_uuid']['S'],
                'user_display_name': item['user_display_name']['S'],
                'user_handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': item['sk']['S']
            })
        print(results)    
        return results    

    def display_messages(client, tableName, message_group_uuid):
        year = str(datetime.now().year)
        table_name = tableName
        query_string = {
        'TableName': table_name,
        'KeyConditionExpression': 'pk = :pkval AND begins_with(sk,:skval)',
        'ScanIndexForward': False,
        'ExpressionAttributeValues': {
            ':skval': {'S': year },
            ':pkval': {'S': f"MSG#{message_group_uuid}"}
        }
        }

        response = client.query(**query_string)
        items = response['Items']
        #items.reverse()
        results = []
        print('items', items)
        for item in items:
            print('debug item',item)
            created_at = item['sk']['S']
            results.append({
                'message_group_uuid': item['message_uuid']['S'],
                'user_display_name': item['user_display_name']['S'],
                'user_handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': created_at
            })
        return results

    def create_message(client, tableName, message_group_uuid, message, user_uuid, user_display_name=None, user_handle=None):
        table_name = tableName
        pkval = f"MSG#{message_group_uuid}"
        skval = datetime.now().isoformat()
        message_uuid = str(uuid.uuid4())
        #skval = now
        item = {
            'pk': {'S': pkval},
            'sk': {'S': skval},
            'message': {'S': message},
            'user_uuid': {'S': user_uuid},
            'message_uuid': {'S': message_uuid},
            'user_display_name': {'S': user_display_name},
            'user_handle': {'S': user_handle}
        }

        response = client.put_item(
            TableName=table_name,
            Item=item
        )

# Print the response from DynamoDB
        print(response)
        return {
            'message_group_uuid': message_group_uuid,
            'message': message,
            'user_uuid': user_uuid,
            'pk': pkval,
            'sk': skval,
            'user_handle': user_handle,
            'user_display_name': user_display_name

        }

    def create_message_group(client, tableName, message, my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
        print('message_groups ddb', tableName)
        table_name          = tableName
        message_group_uuid  = str(uuid.uuid4())
        message_uuid        = str(uuid.uuid4())
        now                 = str(datetime.now().astimezone().isoformat())
        created_at          = now
        print('message_groups ddb', table_name)
        my_message_group = {
            'pk': {'S': f'GRP#{my_user_uuid}'},
            'sk': {'S': f'{created_at}'},
            'user_display_name': {'S': other_user_display_name},
            'user_uuid': {'S': other_user_uuid},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_handle': {'S': other_user_handle}
        }

        other_message_group = {
            'pk': {'S': f'GRP#{other_user_uuid}'},
            'sk': {'S': f'{created_at}'},
            'user_display_name': {'S': my_user_display_name},
            'user_uuid': {'S': my_user_uuid},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_handle': {'S': my_user_handle}
        }

        message_group = {
            'pk': {'S': f'MSG#{message_group_uuid}'},
            'sk': {'S': f'{created_at}'},
            'message_uuid': {'S': message_uuid},
            'user_handle': {'S': my_user_handle},
            'user_display_name': {'S': my_user_display_name},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid}
        }

        put_requests = {
            table_name: [
            {'PutRequest': {'Item': my_message_group}},
            {'PutRequest': {'Item': other_message_group}},
            {'PutRequest': {'Item': message_group}}
            ]
        }
        # Batch write the items
        try:
            response = client.batch_write_item(RequestItems=put_requests)
            print('batch response', response)
            return {
            'message_group_uuid': message_group_uuid
            }
        except botocore.exceptions.ClientError as e:
            print('== create_message_group.error')
            print(e)
