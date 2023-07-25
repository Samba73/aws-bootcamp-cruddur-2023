
from datetime import datetime, timedelta, timezone
from lib.ddb import DDB
from lib.db_new import db
import logging
import os
import uuid


class CreateMessage:
    def run(trans, cognito_user_id, message, handle=None, message_group_uuid=None):
        model = {
            'errors': None,
            'data': None
        }

        if (trans == "update"):
            if message_group_uuid == None or len(message_group_uuid) < 1:
                model['errors'] = ['message_group_uuid_blank']

        if cognito_user_id == None or len(cognito_user_id) < 1:
            model['errors'] = ['cognito_user_id_blank']

        if (trans == "new"):
            if handle == None or len(handle) < 1:
                model['errors'] = ['user_reciever_handle_blank']

        if message == None or len(message) < 1:
            model['errors'] = ['message_blank']
        elif len(message) > 1024:
            model['errors'] = ['message_exceed_max_chars_1024']

        if model['errors']:
            # return what we provided
            model['data'] = {
                'error': "Error in data"
            }

        # sql = extract_query('messages', 'create_message_user')
        sql = db.extract_query('messages', 'create_message_user')
        print('the sql is', sql)

        if handle:
            user = db.query_execution_array(sql, {
                'cognito_user_id': cognito_user_id,
                'user_receiver_handle': handle
            })
            print('item is', user)
            for item in user:
                if item['kind'] == 'sender':
                    my_user = item
                elif item['kind'] == 'recv':
                    other_user = item

        else:

            user = db.query_execution_array(sql, {
                'cognito_user_id': cognito_user_id,
                'user_receiver_handle': ''
            })
            # for item in user:
            #   if item['kind'] == 'sender':
            #     my_user = item
            #   elif item['kind'] == 'recv':
            #     other_user = item
            print('new message user', user)
        # my_user = next((item for item in user if item["kind"] == 'sender'),None)
        # other_user = next((item for item in user if item["kind"] == 'recv'),None)

        ddb = DDB.client()
        if trans == 'update':
            message = DDB.create_message(
                client=ddb, tableName=os.getenv("DDBTABLENAME"),
                message_group_uuid=message_group_uuid,
                message=message, user_uuid=user[0]['uuid'],
                user_handle=user[0]['handle'], user_display_name=user[0]['display_name'])

        if trans == 'new':
            message = DDB.create_message_group(
                client=ddb, tableName=os.getenv("DDBTABLENAME"),
                message=message, my_user_uuid=my_user['uuid'],
                my_user_display_name=my_user['display_name'],
                my_user_handle=my_user['handle'],
                other_user_uuid=other_user['uuid'],
                other_user_display_name=other_user['display_name'],
                other_user_handle=other_user['handle'])

        model['data'] = message
        print('create_message model', model)
        return model
