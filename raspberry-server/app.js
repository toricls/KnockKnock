const fs = require('fs');
const path = require('path');
const http = require('http');
const app = require('express')();
const server = http.createServer();
const port = process.env.PORT || 5656;
const morgan = require('morgan');
const logger = morgan('combined');
const axios = require('axios');
const exec = require('child_process').exec;
const sys = require('sys')
const bodyParser = require('body-parser');
app.use(bodyParser.json());
const PythonShell = require('python-shell');

const options = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: '../camera',
  // args: ['value1', 'value2', 'value3']
};

app.post('/sound', (req, res, next) => {
  const { mp3URL } = req.body;
  exec(`mpg123 ${mp3URL}`, (error, stdout, stderr) => {
    if (error) return next(error);
    sys.print('stdout: ' + stdout);
    sys.print('stderr: ' + stderr);
    console.log(error);
    console.log('Succcess!!!!!!!!');
    res.send({ result: 'Success!' });
  });
});

app.get('/wave', (req, res) => {
  PythonShell.run('wave.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution 

    res.send({ result: 'Success!' });
  });
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
