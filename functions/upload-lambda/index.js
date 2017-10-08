const ENV = process.env.ENV;
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const queryString = require('query-string');

// Expecting `name` and `type` will be provided as query paramters of API call's
exports.handler = (event, context, callback) => {
  let params = queryString.parse(event.body);
  let s3Params = {
    Bucket: process.env.BUCKET_NAME,
    Key:  params.name,
    ContentType: params.type,
    ACL: 'public-read',
  };
  let uploadURL = s3.getSignedUrl('putObject', s3Params);

  callback(null, {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify({ uploadURL: uploadURL }),
  })
};