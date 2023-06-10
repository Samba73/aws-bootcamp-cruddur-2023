#from psycopg_pool import ConnectionPool
import os
import sys
import re
import psycopg2
from psycopg2 import pool

class Db:
    def __init__(self):
        self.init_connection()
    
    def query_wrap_object(self, template):
        sql = f"""
        (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
        {template}
        ) object_row);
        """
        return sql

    def query_wrap_array(self, template):
        sql = f"""
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
        {template}
        ) array_row);
        """
        return sql
    
    def init_connection(self):
      # sample entries
        #db_host = 'cruddur-db.cyzqxlnlmrnn.ap-southeast-1.rds.amazonaws.com'  # Replace with the host endpoint of your RDS instance
        #db_port = '5432'  # Replace with the port number of your RDS instance
        #db_name = 'cruddur'  # Replace with the name of your database
        #db_user = 'cruddurroot'  # Replace with your database username
        #db_password = 'Password999'  # Replace with your database password
        db_host = os.getenv('POSTGRES_HOST')
        db_port = int(os.getenv('POSTGRES_PORT')) 
        db_name = os.getenv('POSTGRES_DBNAME') 
        db_user = os.getenv('POSTGRES_UNAME')  
        db_password = os.getenv('POSTGRES_PWD') 

        connection_url = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"
        #connection_url=os.getenv("CONNECTION_URL")
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=connection_url)
    
    def extract_query(self, folder, file):
        file = file + ".sql"
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.abspath(os.path.join(current_path, '..'))
        print(parent_path)
        sys.path.append(parent_path)
        #path = os.getcwd()
        #print(path)
        filepath = os.path.join(parent_path, 'queries', folder, file)
        print(filepath)
        with open(filepath, "r") as file:
            sql = file.read()
        print(sql)    
        return sql        
    
    def print_params(self, params):
        blue = '\033[94m'
        no_color = '\033[0m'
        print(f'{blue} SQL Parameters:{no_color}')
        for key, value in params.items():
            print(f'{key}:, {value}')
            
    def print_sql(self, title, sql, params={}):
        cyan = '\033[96m'
        no_color = '\033[0m'
        print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
        print(f'The sql query is: {sql}')
        if params != {}:
            blue = '\033[94m'
            no_color = '\033[0m'
            print(f'{blue} Parameters for above SQL are:{no_color}')
            for key, value in params.items():
                print(f'{key}:{value}')    
                
    def query_insert(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('Insert query with return value', sql, params)
        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql)
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if is_returning_id:
                    returning_value = cur.fetchone()[0]
                conn.commit()
                if is_returning_id:
                    return returning_value
        except Exception as err:
            self.print_sql_err(err)
        finally:
            self.pool.putconn(conn)
                   
    def query_execution_array(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('SQL Execution, array result', sql, params)
        wrapped_sql = self.query_wrap_array(sql)
        print(wrapped_sql)
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                print(json)
                return json[0]
        finally:
            self.pool.putconn(conn)
        
    def query_execution_object(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql('SQL Execution, object return', sql, params)
        wrapped_sql = self.query_wrap_object(sql)
        print(wrapped_sql)
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                if json is None:
                    return "{}"
                else:
                    return json[0]
        finally:
            self.pool.putconn(conn)
            
    def query_value(self, sql, params={}, verbose=True):
        if verbose:
            self.print_sql("Extract value", sql, params)
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                json = cur.fetchone()
                return json[0]
        finally:
            self.pool.putconn(conn)
    
    def print_sql_err(self, err):
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
      
db = Db()      