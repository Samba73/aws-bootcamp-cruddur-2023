"use strict";
const { CognitoJwtVerifier } = require("aws-jwt-verify");

const jwtVerifier = CognitoJwtVerifier.create({
  userPoolId: process.env.USER_POOL_ID,
  tokenUse: "access",
  clientId: process.env.CLIENT_ID,

});

exports.handler = async (event) => {
  console.log("request:", JSON.stringify(event, undefined, 2));
  const token = JSON.stringify(event.headers["authorization"]).split(" ")[1].replace(/['"]+/g, '');

  try {
    const payload = await jwtVerifier.verify(token);
    console.log('payload', payload);
    console.log("Access allowed. JWT payload:", payload);
  } catch (err) {
    console.error("Access forbidden:", err);
    return {
      isAuthorized: false,
    };
  }
  return {
    isAuthorized: true,
  };
};

