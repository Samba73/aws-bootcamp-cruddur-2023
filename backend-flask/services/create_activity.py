import uuid
from datetime import datetime, timedelta, timezone
from lib.db_new import db
class CreateActivity:
  def run(message, cognito_user_id, ttl):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['user_cognito_id_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'cognito_user_id':  cognito_user_id,
        'message': message
      }   
    else:
      print('activity', cognito_user_id)
      query          = db.extract_query('activities', 'create')
      returning_uuid = db.query_insert(query, {
        'cognito_user_id': cognito_user_id,
        'message': message,
        'expires_at': (now + ttl_offset).isoformat()
      })
      print('returning uuid', returning_uuid)
      activity_query = db.extract_query('activities', 'select')
      print(activity_query)
      activity = db.query_execution_object(activity_query, {
        'uuid': returning_uuid
      })
      model["data"] = activity
    return model