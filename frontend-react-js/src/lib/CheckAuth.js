import { Auth } from 'aws-amplify';
inport { resolvePath } from 'react-router-dom';

export async function getAuth() => {
  Auth.currentSession()
  .then((cognito_user_session) => {
      access_token = cognito_user_session.accessToken.jwtToken
      localStorage.setItem("access_token", access_token)  
  })
  .catch((err) => console.log(err));
};

export async function checkAuth(setUser) => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
    return Auth.currentSession()
  }).then((cognito_user_session) => {
      console.log(cognito_user_session)
      localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken)
  })
  .catch((err) => console.log(err));
};
