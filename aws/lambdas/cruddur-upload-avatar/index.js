"use strict"
const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()
const URL_EXPIRATION_SECONDS = 300
const token =
  "eyJraWQiOiJvWUtqTklIclpoK1htZ0JnQTJjV1J1aGFpaUdJWHpIVmI1U0psY1pSUU40PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwMzQ2ZWFjZS1jZTM3LTQ3NzMtYmJmNy0wMGIxZWE1YjljZWQiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGhlYXN0LTFfbmlvRE1LdFlmIiwiY2xpZW50X2lkIjoiNGdsMm81OG8zM29kdjU2ZDByc21uZXFlbzkiLCJvcmlnaW5fanRpIjoiNWNkNjEzZDItYzg4ZC00MzkwLTlmYjItMzQ4Y2M3NWVmMGZhIiwiZXZlbnRfaWQiOiIxYjZjMTk1Yy0xODNkLTQ1MDItODk1OC1jY2Q3MjlhY2M4ODEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjgzOTUyNzkxLCJleHAiOjE2ODM5NTYzOTEsImlhdCI6MTY4Mzk1Mjc5MSwianRpIjoiMTJiZGYyNTMtZmEzYS00M2NmLTgyOTUtZjkzMTA0YWRlNjljIiwidXNlcm5hbWUiOiIwMzQ2ZWFjZS1jZTM3LTQ3NzMtYmJmNy0wMGIxZWE1YjljZWQifQ.CZbxaFISkPIPgFH89Zg4vraIV2beHNMfiPgbeqfD0qUjHh-llqAjbMOUqN8cScZREyMWNhJCpFndH79ByM-Z5Xn6blvPGSwERcwwgHVbe3onH2fridPPKhJ16y2s-u7AtyuXOZH0vN46M3SszPcsEMlRfTrRbuxHsjOpHShCbuC1VnzIlTNuHLmrw0tr19muHpkYj-WGRcMWiZbuhqJ_PGqLTR6UVwcUa05kBWdKk_0N6nwTW8OR4Pn5R71uMWxoKHc-T13M2uiJ4kgSSB32KieMrzdjqO2fnF0_rmXsVBZYpVSYTVmQ3K8ca-RKLw8gdBbME6uCvjA3x0Afxbq47Q"
exports.handler = async (event) => {
  return await getUploadURL(event)
}

const getUploadURL = async function(event) {
  console.log('event', event)
  const eventToken = JSON.stringify(event.headers["authorization"]).split(" ")[1].replace(/['"]+/g, '')
  const decodedToken = JSON.parse(
    Buffer.from(eventToken.split(".")[1], "base64").toString()
  )  
  //const decodedToken = jwtDecode(token)
  console.log('decodeToken', decodedToken)
  const cognito_user_id = decodedToken['sub']
  console.log('cognito', cognito_user_id)
  const randomID = parseInt(Math.random() * 10000000)
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
getUploadURL()
