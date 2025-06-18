import redis from 'redis';

// Create Redis client for publisher
const publisher = redis.createClient();

// Handle successful connection
publisher.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle connection error
publisher.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Function to publish message after specified time
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish('ALXchannel', message);
  }, time);
}

// Call publishMessage with the specified messages and times
publishMessage('ALX Student #1 starts course', 100);
publishMessage('ALX Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('ALX Student #3 starts course', 400);
