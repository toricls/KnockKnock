const ENV = process.env.ENV;

module.exports = (event, context, callback) => {
  console.log(event);
  return context.fail('Login Failed.');
};
