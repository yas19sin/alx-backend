import redis from 'redis';

// Create Redis client
const client = redis.createClient();

// Handle successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle connection error
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Create Hash - store values in ALX hash
client.hset('ALX', 'Portland', 50, redis.print);
client.hset('ALX', 'Seattle', 80, redis.print);
client.hset('ALX', 'New York', 20, redis.print);
client.hset('ALX', 'Bogota', 20, redis.print);
client.hset('ALX', 'Cali', 40, redis.print);
client.hset('ALX', 'Paris', 2, redis.print);

// Display Hash - get all values from ALX hash
client.hgetall('ALX', (err, result) => {
  if (err) {
    console.log(err);
  } else {
    console.log(result);
  }
});
