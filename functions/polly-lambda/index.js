const AWS = require('aws-sdk');
const Polly = new AWS.Polly();
const S3 = new AWS.S3();

module.exports = (event, context, callback) => {
  console.log(event);
  const params = {
    Text: event.text,
    OutputFormat: 'mp3',
    VoiceId: 'Kimberly'
  };

  Polly.synthesizeSpeech(params, (err, data) => {
    if (err) {
      console.log(err.code);
      callback(err);
    } else if (data) {
      if (data.AudioStream instanceof Buffer) {
        const timstamp = new Date().getTime();
        const s3Params = {
          Bucket: process.env.BUCKET_NAME,
          Key: timstamp + '.mp3',
          ContentType: 'audio/mpeg',
          ACL: 'public-read',
          Body: data.AudioStream
        };
        S3.putObject(s3Params, (errS3) => {
          if (errS3) {
            console.log(errS3);
            callback(errS3);
          } else {
            callback(null, 'done');
          }
        });
      }
    }
  });
};
