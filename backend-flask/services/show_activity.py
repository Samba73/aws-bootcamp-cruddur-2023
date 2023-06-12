from datetime import datetime, timedelta, timezone
from lib.db_new import db
class ShowActivities:
  def run(activity_uuid):
    now = datetime.now(timezone.utc).astimezone()
    query = db.extract_query('activities', 'show')
    activities = db.query_execution_array(query , {
      'uuid': activity_uuid
    })
    return activities