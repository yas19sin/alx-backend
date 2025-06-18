import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();
const port = 1245;

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);

// Initialize variables
let reservationEnabled = true;

// Function to reserve seats
function reserveSeat(number) {
  client.set('available_seats', number);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
}

// Initialize available seats to 50
reserveSeat(50);

// Route to get available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat')
    .save((err) => {
      if (err) {
        return res.json({ status: 'Reservation failed' });
      }
      res.json({ status: 'Reservation in process' });
      return undefined;
    });

  // Handle job completion
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  // Handle job failure
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });

  return undefined;
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the reserve_seat queue
  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();
      const newSeats = currentSeats - 1;

      if (newSeats === 0) {
        reservationEnabled = false;
      }

      if (newSeats >= 0) {
        reserveSeat(newSeats);
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    } catch (error) {
      done(error);
    }
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
