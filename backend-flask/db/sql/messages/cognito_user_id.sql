SELECT 
      users.uuid,
      users.display_name,
      users.handle
    FROM users
    WHERE
      users.uuid = %(cognito_user_id)s