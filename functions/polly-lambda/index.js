const AWS = require('aws-sdk');
const Polly = new AWS.Polly();
const S3 = new AWS.S3();

module.exports = (event, context, callback) => {
  let params = JSON.parse(event.body);
  const voiceId = params.gender && params.gender === 'male' ? 'Karl' : 'Kimberly';
  const pollyParams = {
    Text: params.text,
    OutputFormat: 'mp3',
    VoiceId: voiceId
  };

  Polly.synthesizeSpeech(pollyParams, (err, data) => {
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
        S3.upload(s3Params, (errS3, dataS3) => {
          if (errS3) {
            console.log(errS3);
            callback(errS3);
          } else {
            const mp3SSLURL = dataS3.Location;
            const mp3URL = mp3SSLURL.replace('https://', 'http://');
            callback(null, {
              statusCode: 201,
              headers: {
                'Access-Control-Allow-Origin': '*'
              },
              body: JSON.stringify({ mp3SSLURL, mp3URL }),
            });
          }
        });
      }
    }
  });
};
