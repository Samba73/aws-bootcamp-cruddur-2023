from datetime   import datetime, timedelta, timezone
from lib.ddb    import DDB
from lib.db_new import db

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
      sql = db.extract_query('users','userProfile')
      results = db.query_execution_object(sql,{'handle': user_handle})
      model['data'] = results
    return model
