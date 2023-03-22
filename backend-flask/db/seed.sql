INSERT INTO public.users(display_name, handle, cognito_user_id) VALUES 
('Samba K', 'samba', 'dummy');

INSERT INTO public.activities(user_uuid, message, expires_at) VALUES 
((select uuid from public.users where users.handle='samba' LIMIT 1),'Test message',
current_timestamp + interval '10 day' );