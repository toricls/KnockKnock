const ENV = process.env.ENV;
const AWS = require('aws-sdk');
const S3 = new AWS.S3();

// Expecting `name` and `type` will be provided as request body paramters of API call's
module.exports = (event, context, callback) => {
  //console.log(event)
  let params = JSON.parse(event.body);
  let s3Params = {
    Bucket: process.env.BUCKET_NAME,
    Key: params.name,
    ContentType: params.type,
    ACL: 'public-read',
  };
  let uploadURL = S3.getSignedUrl('putObject', s3Params);

  callback(null, {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify({ uploadURL }),
  })
};
