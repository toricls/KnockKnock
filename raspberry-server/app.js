const fs = require('fs');
const http = require('http');
const app = require('express')();
const server = http.createServer();
const volleyball = require('volleyball');
const port = process.env.PORT || 5656;


app.get('/', (req, res) => {
  res.send({ result: 'Success!' });
});

server.on('request', app);

server.listen(port, () => {
  console.log(`The server is listening on port ${port}!`);
});

module.exports = app;
