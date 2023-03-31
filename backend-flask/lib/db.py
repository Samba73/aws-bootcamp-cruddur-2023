from psycopg_pool import ConnectionPool
import os, sys
import re

#connection_url = os.getenv("PROD_CONNECTION_URL")
connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)

def query_wrap_select(template):
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


def query_execution_array(sql, params={}):
  wrapped_sql = query_wrap_array(sql)
  print(wrapped_sql)
  try:
    #connection_url = os.getenv("PROD_CONNECTION_URL")
    connection_url = os.getenv("CONNECTION_URL")
    pool = ConnectionPool(connection_url)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()
        print(json)
        return json[0]
  except Exception as err:
    print_sql_err(err)
  finally:
    if conn is not None:
      cur.close()
      conn.close()            

def query_execution_select(sql, params={}):
  wrapped_sql = query_wrap_array(sql)
  print(wrapped_sql)
  print(params)
  try:
    #connection_url = os.getenv("PROD_CONNECTION_URL")
    connection_url = os.getenv("CONNECTION_URL")
    pool = ConnectionPool(connection_url)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()
        if json is None:
          return "{}"
        else:
          return json[0]
  except Exception as err:
    print_sql_err(err)
  finally:
    if conn is not None:
      cur.close()
      conn.close()  

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

def query_insert(sql, params={}):
  pattern = r"\bRETURNING\b"

  is_returning_id = re.search(pattern, sql)

  try:
    #connection_url = os.getenv("PROD_CONNECTION_URL")
    connection_url = os.getenv("CONNECTION_URL")
    pool = ConnectionPool(connection_url)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql, params)
        if is_returning_id:
          uuid = cur.fetchone()[0]
          return uuid
        conn.commit()  
  except Exception as err:
    print_sql_err(err)
  finally:    
    if conn is not None:
      cur.close()
      conn.close()


def print_sql_err(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
