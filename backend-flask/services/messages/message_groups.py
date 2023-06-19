from datetime   import datetime, timedelta, timezone
from lib.ddb    import DDB
from lib.db_new import db
import logging, os
class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }
  
    sql = db.extract_query('messages', 'cognito_user_id')
 
    user_id = db.query_value(sql, {
      'cognito_user_id': cognito_user_id
    })
    print('new is', user_id)
    ddb = DDB.client()
    message_groups = DDB.display_message_groups(ddb, os.getenv("DDB_TABLENAME"), user_id)
    model['data'] = message_groups
    print('model', model)
    return model