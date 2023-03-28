from datetime import datetime, timedelta, timezone
class Messages:
  def run(cognito_user_id, message_group_uuid):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    sql = extract_query('messages', 'cognito_user_id')
    user_id = query_execution_select(sql, {
      'cognito_user_id': cognito_user_id
    })
    
    ddb = DDB.client()
    message_groups = DDB.display_message(ddb, message_group_uuid)
    model['data'] = message_groups
    print('model', model)
    return model