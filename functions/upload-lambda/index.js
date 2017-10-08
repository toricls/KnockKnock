const ENV = process.env.ENV;
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const queryString = require('query-string');

exports.handler = (event, context, callback) => {
  let params = queryString.parse(event.body);
  let s3Params = {
    Bucket: process.env.BUCKET_NAME,
    Key:  params.name,
    ContentType: params.type,
    ACL: 'public-read',
  };


  // return context.fail('Login Failed.');
};
