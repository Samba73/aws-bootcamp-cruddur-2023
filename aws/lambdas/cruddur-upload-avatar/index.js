'use strict';
const AWS = require('aws-sdk');
const fs = require('fs');

const s3 = new AWS.S3({
  region: process.env.AWS_DEFAULT_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  signatureVersion: 'v4'
});

// Change this value to adjust the signed URL's expiration
const URL_EXPIRATION_SECONDS = 300;

const main = async () => {
  const randomID = parseInt(Math.random() * 10000000);
  const Key = `${randomID}.jpg`;

  // Get signed URL from S3
  const s3Params = {
    Bucket: 'uploaded-avatars',
    Key,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: 'image/jpeg'
  };

  console.log('Params: ', s3Params);
  const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params);
  console.log(uploadURL);

  // Write the presigned URL to a file
  fs.writeFileSync('presignedurl.txt', uploadURL);
};

main();
