from datetime import datetime, timedelta, timezone
from lib.db import extract_query, query_execution_select, query_insert
from lib.ddb import DDB
import logging
from lib.db_new import db
class Messages:
  def run(cognito_user_id, message_group_uuid):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()
    print('message_group_uuid',message_group_uuid)
    #sql = extract_query('messages', 'cognito_user_id')
    sql = db.extract_query('messages', 'cognito_user_id')
    """
    user_id = query_execution_select(sql, {
      'cognito_user_id': cognito_user_id
    })
    """
    user_id = db.query_execution_object(sql, {
      'cognito_user_id': cognito_user_id
    })
    ddb = DDB.client()
    message_groups = DDB.display_messages(ddb, message_group_uuid)
    model['data'] = message_groups
    print('messages model', model)
    return model