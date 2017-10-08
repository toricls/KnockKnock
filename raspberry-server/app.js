const fs = require('fs');
const path = require('path');
const http = require('http');
const app = require('express')();
const server = http.createServer();
const volleyball = require('volleyball');
const port = process.env.PORT || 5656;
const morgan = require('morgan');

const logger = morgan('combined');

app.get('/', (req, res) => {
  console.log('Test');
  res.send({ result: 'Success!' });
});

app.use(logger);

app.use((req, res, next) => {
  if (path.extname(req.path).length > 0) {
    res.status(404).end();
  } else {
    next(null);
  }
});

server.on('request', app);

server.listen(port, () => {
  console.log(`The server is listening on port ${port}!`);
});

module.exports = app;
