from lib.db import extract_query, query_execution_array, query_insert, query_execution_select
from lib.db_new import db
class UpdateProfile:
  def run(cognito_user_id,bio,display_name):
    model = {
      'errors': None,
      'data': None
    }

    if display_name == None or len(display_name) < 1:
      model['errors'] = ['display_name_blank']

    if model['errors']:
      model['data'] = {
        'bio': bio,
        'display_name': display_name
      }
    else:
      handle = UpdateProfile.update_profile(bio,display_name,cognito_user_id)
      data = UpdateProfile.query_users_short(handle)
      model['data'] = data
    return model
  
  def update_profile(bio,display_name,cognito_user_id):
    if bio == None:    
      bio = ''

    #sql = extract_query('users','update')
    sql = db.extract_query('users','update')
    """
    handle = query_insert(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })
    """
    handle = db.query_insert(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })
  def query_users_short(handle):
    #sql = extract_query('users','short')
    sql = db.extract_query('users','short')
    """
    data = query_execution_select(sql,{
      'handle': handle
    })
    """
    data = db.query_execution_object(sql,{
      'handle': handle
    })
    return data
