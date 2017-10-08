const ENV = process.env.ENV;

exports.handler = (event, context, callback) => {
  return context.fail('Login Failed.');
};
