import redis from 'redis';

// Create Redis client for subscriber
const subscriber = redis.createClient();

// Handle successful connection
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle connection error
subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Subscribe to ALXchannel
subscriber.subscribe('ALXchannel');

// Handle messages received on the channel
subscriber.on('message', (channel, message) => {
  console.log(message);

  // If message is KILL_SERVER, unsubscribe and quit
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe('ALXchannel');
    subscriber.quit();
  }
});
