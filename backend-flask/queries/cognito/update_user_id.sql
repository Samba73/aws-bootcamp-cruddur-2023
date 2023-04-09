UPDATE public.users
    SET cognito_user_id = %(cognito_user_id)s
    WHERE handle = %(handle)s