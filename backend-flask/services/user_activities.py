from datetime import datetime, timedelta, timezone
from lib.db import extract_query, query_execution_select, query_insert
from lib.ddb import DDB

class UserActivities:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      sql = extract_query('messages','userProfile')
      results = query_execution_select(sql,{'handle': user_handle})
      model['data'] = results
    return model
