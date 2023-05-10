"use strict"
const jwtDecode = require('jwt-decode')
const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()
const URL_EXPIRATION_SECONDS = 300

// Main Lambda entry point
exports.handler = async (event) => {
  return await getUploadURL(event)
}

const getUploadURL = async function(event) {
  console.log('event', event)
  const token = JSON.stringify(event.headers["authorization"]).split(" ")[1].replace(/['"]+/g, '')
  const decodedToken = jwtDecode(token)
  console.log('decodeToken', decodedToken)
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
    "Access-Control-Allow-Origin": "https://samba73-awsbootcampcrud-pmsk2pldufg.ws-us97.gitpod.io",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
  }
  const statusCode = 200
  
  return ({
    body: JSON.stringify(body),
    headers,
    statusCode
  })
}
