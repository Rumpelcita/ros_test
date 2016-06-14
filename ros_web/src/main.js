ros = new ROSLIB.Ros();

// Check for backend errors
ros.on('error', function(error) {
  console.log(error);
});

// Check connection status
ros.on('connection', function() {
  console.log('Connection made!');
});
ros.on('close', function() {
  console.log('Connection closed.');
});

// Connect to rosbridge WebSocket server.
var connectionUrl = 'ws://localhost:8080';

console.log(connectionUrl);
ros.connect(connectionUrl);

// Configure connections to turtlesim Topics & Services

// Connect with the turtle position so we can draw it on the canvas
turtle_pose = new ROSLIB.Topic({
  ros : ros,
  name : '/turtle1/pose',
  messageType : 'turtlesim/Pose'
});

// Service connection for turtlesim reset
reset_turtle = new ROSLIB.Service({
  ros : ros,
  name : '/reset',
    serviceType : 'std_srvs/Empty'
});

// Position variables
var pos = {
  x : 0, 
  y : 0,
  z : 0,
  li: 0,
  av: 0,
  t : 0
};
var oldX;
var oldY;

// Subscription to turtle_pose topic
turtle_pose.subscribe(function(message) {
    if (message.x != pos.x || message.y != pos.y || message.z != pos.z || message.theta != pos.t ||
    message.linear_velocity != pos.li || message.angular_velocity != pos.av){
        pos.x = message.x;
        pos.y = message.y;
        pos.z = message.z;
        pos.t = message.theta;
        pos.li = message.linear_velocity;
        pos.av = message.angular_velocity;
        draw_trutle_path(pos);
    }
});

// Draws the canvas according to turtlesim position
draw_trutle_path = function (message) {
  var canvas_size = 350;
  var zoom = canvas_size / 12;
  var x = message.x * zoom;
  var y = canvas_size - message.y * zoom;
  
  var c = document.getElementById("turtle");
  var ctx = c.getContext("2d");
  ctx.beginPath();
  if (!oldX || !oldY){
    oldX = x;
    oldY = y;  
  }
  ctx.moveTo(oldX, oldY);
  ctx.lineTo(x, y);
  oldX = x;
  oldY = y;
  ctx.stroke();
};

reset_position = function(){
  oldX = null;
  oldY = null;
};
