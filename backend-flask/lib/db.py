from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("PROD_CONNECTION_URL")
pool = ConnectionPool(connection_url)

def query_execution(folder, file):
  print(folder)
  print(file)
  sql = extract_query(folder, file)
  with pool.connection() as conn:
    with conn.cursor() as cur:
      cur.execute(sql)
      json = cur.fetchone()
  return json    

def extract_query(folder, file):
  file = file + ".sql"
  path = os.getcwd()
  print(path)
  filepath = os.path.join(path, 'db','sql', folder, file)
  print(filepath)
  with open(filepath, "r") as file:
    sql = file.read()
  print(sql)    
  return sql    