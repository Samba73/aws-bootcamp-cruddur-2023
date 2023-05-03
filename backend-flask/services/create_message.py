import uuid
from datetime import datetime, timedelta, timezone
from lib.db import extract_query, query_execution_select, query_insert
from lib.ddb import DDB
import logging

class CreateMessage:
  def run(trans,cognito_user_id, message, handle=None, message_group_uuid=None):
    model = {
      'errors': None,
      'data': None
    }

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    sql = extract_query('messages', 'create_message_user')
    print('the sql is', sql)
    if handle:
      user = query_execution_array(sql, {
        'cognito_user_id': cognito_user_id,
        'user_receiver_handle': handle
      })    
      for item in user:
        if item['kind'] == 'sender':
          my_user = item
        elif item['kind'] == 'recv':
          other_user = item  

    else:
      user = query_execution_array(sql, {
        'cognito_user_id': cognito_user_id,
        'user_receiver_handle': ''  
      })  
      # for item in user:
      #   if item['kind'] == 'sender':
      #     my_user = item
      #   elif item['kind'] == 'recv':
      #     other_user = item  
    print('user', user)
    #my_user = next((item for item in user if item["kind"] == 'sender'),None)
    #other_user = next((item for item in user if item["kind"] == 'recv'),None)
    
    ddb = DDB.client()
    if trans == 'update':
      message = DDB.create_message(
        client=ddb, message_group_uuid=message_group_uuid,
        message=message, user_uuid=user[0]['uuid'],
        user_handle=user[0]['handle'], user_display_name=user[0]['display_name'] )

    if trans == 'new':
      message = DDB.create_message_group(
        client=ddb, message=message, my_user_uuid=my_user['uuid'],
        my_user_display_name=my_user['display_name'], 
        my_user_handle=my_user['handle'], 
        other_user_uuid=other_user['uuid'], 
        other_user_display_name=other_user['display_name'], 
        other_user_handle=other_user['handle'])    

    model['data'] = message
    print('create_message model', model)
    return model
    