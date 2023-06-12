import uuid
from datetime import datetime, timedelta, timezone
from lib.db_new import db
class CreateReply:
  def run(message, cognito_user_id, activity_uuid):
    model = {
      'errors': None,
      'data': None
    }

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if activity_uuid == None or len(activity_uuid) < 1:
      model['errors'] = ['activity_uuid_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      # return what we provided
      model['data'] = {
        'message': message,
        'reply_to_activity_uuid': activity_uuid
      }
    else:
      now = datetime.now(timezone.utc).astimezone()
      reply_query = db.extract_query('activities', 'reply')
      
      reply_id = db.query_insert(sql)(reply_query, {
        'cognito_user-id': cognito_user_id,
        'message': message,
        'reply_to_activity_uuid': activity_uuid
      })
      
      display_reply = db.extract_query('activities', 'select')
      reply = db.query_execution_object(display_reply, {
        'uuid': reply_id
      })     
      model['data'] = reply                                    
  return model