import psycopg2
import json
import os


def lambda_handler(event, context):
    user    = event['request']['userAttributes']
    print('A-----')
    print(event['request']['userAttributes'])
    print('B-----')
    print(user)
    user_displayname            =   user['name']
    user_email                  =   user['email']
    user_handle                 =   user['preferred_username']
    user_cognito_id             =   user['sub']
    
    try:
        sql = f"""
            INSERT INTO public.users (
                                        display_name, 
                                        email,
                                        handle, 
                                        cognito_user_id
                                    ) 
            VALUES(%s,%s,%s,%s)
        """
        print('C------')
        print(sql)
        conn = psycopg2.connect(os.getenv('PROD_CONN_STRING'))
        print(conn)
        cur = conn.cursor()
        print(cur)
        params = [
            user_displayname,
            user_email,
            user_handle,
            user_cognito_id
        ]
        print(params)
        cur.execute(sql,params)
        conn.commit()
        print('committed')
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return event     