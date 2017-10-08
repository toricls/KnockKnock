const fs = require('fs');
const path = require('path');
const http = require('http');
const app = require('express')();
const server = http.createServer();
const port = process.env.PORT || 5656;
const morgan = require('morgan');
const logger = morgan('combined');

const PythonShell = require('python-shell');

const options = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: '../camera',
  // args: ['value1', 'value2', 'value3']
};

app.get('/wave', (req, res) => {
  PythonShell.run('wave.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution 

    res.send({ result: 'Success!' });
  });
});

app.get('/sound', (req, res) => {
  
  res.send({ result: 'Success!' });
});

app.get('/light', (req, res) => {
  
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
