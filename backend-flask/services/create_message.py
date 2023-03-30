import uuid
from datetime import datetime, timedelta, timezone
from lib.db import extract_query, query_execution_select, query_insert
from lib.ddb import DDB
import logging

class CreateMessage:
  def run(cognito_user_id, message, message_group_uuid):
    model = {
      'errors': None,
      'data': None
    }

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    sql = extract_query('messages', 'create_message_user')
    user = query_execution_select(sql, {
      'cognito_user_id': cognito_user_id
    })
    #print('user data create message', user)
    ddb = DDB.client()
    message = DDB.create_message(
      client=ddb, message_group_uuid=message_group_uuid,
      message=message, user_uuid=user['uuid'],
      user_handle=user['handle'], user_display_name=user['display_name'] )
    model['data'] = message
    print('create_message model', model)
    return model
    