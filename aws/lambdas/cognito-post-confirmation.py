import psycopg2
import json
import os


def lambda_handler(event, context):
    user = event['request']['userAttributes']

    user_displayname    =   user['name']
    user_email          =   user['email']
    user_handle         =   user['preferred_name']
    user_sub            =   user['sub']

    try:
        sql = """
            INSERT INTO public.users (
                                        display_name, 
                                        email,
                                        handle, 
                                        cognito_user_id
                                    ) 
            VALUES(%s,%s,%s,%s)
        """
        conn = psycopg2.conect(os.getenv('PROD_CONN_STRING'))
        cur = conn.cusor()
        params = [
            user_displayname,
            user_email,
            user_handle,
            user_sub
        ]
        cur.execute(sql,*params)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:    
        if conn is not None:
            cur.close()
            conn.close()
    return event        
