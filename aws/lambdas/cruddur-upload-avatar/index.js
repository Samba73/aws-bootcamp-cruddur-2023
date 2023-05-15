"use strict"
const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()
const URL_EXPIRATION_SECONDS = 300
//const token =
//  "eyJraWQiOiJvWUtqTklIclpoK1htZ0JnQTJjV1J1aGFpaUdJWHpIVmI1U0psY1pSUU40PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwMzQ2ZWFjZS1jZTM3LTQ3NzMtYmJmNy0wMGIxZWE1YjljZWQiLCJpc3MiOi$

exports.handler = async (event) => {
  return await getUploadURL(event)
}

const getUploadURL = async function(event) {
  console.log('event', event)
  if (event['routeKey'] == 'OPTIONS /{proxy+}') {
        headers = {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
      statusCode = 200
    } else {
      const eventToken = JSON.stringify(event.headers["authorization"]).split(" ")[1].replace(/['"]+/g, '');
      const decodedToken = JSON.parse(
      Buffer.from(eventToken.split(".")[1], "base64").toString())
      console.log('decodeToken', decodedToken)
      const cognito_user_id = decodedToken['sub']
      console.log('cognito', cognito_user_id)
      //const randomID = parseInt(Math.random() * 10000000)
      const Key = `${cognito_user_id}.jpg`

      // Get signed URL from S3
      const s3Params = {
      Bucket: 'uploaded-avatars',
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
}
getUploadURL()
