'use strict'

const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.REGION })
const s3 = new AWS.S3({
  accessKeyId: process.env.ACCESS_KEY_ID,
  secretAccessKey: process.env.SECRET_ACCESS_KEY,
  signatureVersion: 'v4'
  })

// Change this value to adjust the signed URL's expiration
const URL_EXPIRATION_SECONDS = 300

// Main Lambda entry point

const main = async () => {

  const randomID = parseInt(Math.random() * 10000000)
  const Key = `${randomID}.jpg`

  // Get signed URL from S3
  const s3Params = {
    Bucket: 'uploaded-avatars',
    Key,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: 'image/jpeg',
  }

  console.log('Params: ', s3Params)
  const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params)
  const body = {uploadURL: uploadURL}
  const headers = {
    "Access-Control-AllowHeaders": "*, Authorization",
    "Access-Control-Allow-Origin": "https://samba73-awsbootcampcrud-mx3o0jvvj17.ws-us97.gitpod.io/",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
  }
  const statusCode = 200
  
  return ({
    body: JSON.stringify(body),
    headers,
    statusCode
  })


  // Write the presigned URL to a file
  fs.writeFileSync('presignedurl.txt', uploadURL);
};

main();
