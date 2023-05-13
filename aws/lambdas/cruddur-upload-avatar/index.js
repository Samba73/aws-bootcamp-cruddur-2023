"use strict"
const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()
const URL_EXPIRATION_SECONDS = 300
const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"// Main Lambda entry point
exports.handler = async (event) => {
  return await getUploadURL(event)
}

const getUploadURL = async function(event) {
  console.log('event', event)
  //const token = JSON.stringify(event.headers["authorization"]).split(" ")[1].replace(/['"]+/g, '')
  const decodedToken = JSON.parse(
    Buffer.from(token.split(".")[1], "base64").toString()
  )  
  //const decodedToken = jwtDecode(token)
  console.log('decodeToken', decodedToken)
  //const cognito_user_id = decodedToken[0]['sub']
  //console.log('cognito', cognito_user_id)
  const randomID = parseInt(Math.random() * 10000000)
  const Key = `${randomID}.jpg`

  // Get signed URL from S3
  const s3Params = {
    Bucket: process.env.UploadBucket,
    Key,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: 'image/jpeg'
  }
  const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params)

  const body = {uploadURL: uploadURL}
  const headers = {
    "Access-Control-AllowHeaders": "*, Authorization",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
  }
  const statusCode = 200
  
  return ({
    body: JSON.stringify(body),
    headers,
    statusCode
  })
}
