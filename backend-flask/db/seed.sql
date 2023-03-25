INSERT INTO public.users(display_name, email, handle, cognito_user_id) VALUES 
('Samba K', 'sambasivam.k@gmail.com', 'samba', 'dummy');
INSERT INTO public.users(display_name, email, handle, cognito_user_id) VALUES 
('Vishnu R', 'vishnup@yahoo.com',  'vishnu', 'dummy');

INSERT INTO public.activities(user_uuid, message, expires_at) VALUES 
((select uuid from public.users where users.handle='samba' LIMIT 1),'Test message',
current_timestamp + interval '10 day' );