from datetime import datetime, timedelta, timezone
from lib.db import extract_query, query_execution_select, query_insert
from lib.ddb import DDB
import logging
class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }
    sql = extract_query('messages', 'cognito_user_id')
    user_id = query_execution_select(sql, {
      'cognito_user_id': cognito_user_id
    })
    
    ddb = DDB.client()
    message_groups = DDB.display_message_groups(ddb, user_id)
    model['data'] = message_groups
    return model