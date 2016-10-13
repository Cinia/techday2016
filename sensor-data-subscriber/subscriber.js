var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var mqtt = require('mqtt')
var client  = mqtt.connect('mqtt://10.50.44.154')

client.on('connect', function () {
  client.subscribe('robot/senses/#')
  console.log("Connected to MQTT")  
})

app.get('/', function(req, res){
  res.sendfile('index.html');
});

io.on('connection', function(socket){
  console.log("io connected")
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
  
  client.on('message', function (topic, message) {
    // message is Buffer 
    io.emit(topic.toString(), message.toString())
})

});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
