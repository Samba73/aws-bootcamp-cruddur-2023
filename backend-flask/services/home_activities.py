from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import query_execution_array, query_execution_select, query_insert, extract_query
from lib.db_new import db
tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None):
    print("HOME ACTIVITY")
    #logger.info("HomeActivities")
    with tracer.start_as_current_span("home-activites-startSpan"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())

      #query = extract_query('activities', 'home')
      query = db.extract_query('activities', 'home')
      #results = query_execution_array(query)
      results = db.query_execution_array(sql=query)
      return results