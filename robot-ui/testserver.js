var express = require('express');
var PORT = 8043;

var app = express();

app.use(function(req, res, next) {
    console.log(req.method, req.path);
    next();
});

app.use(express.static('target'));

app.listen(PORT, function() {
    console.log('Listening on port ' + PORT);
});
