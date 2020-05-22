const { Pool, Client } = require('pg')

const client = new Client({
  user: 'explorer',
  host: '127.0.0.1',
  password: 'outsider',
  database: 'spatial_db',
  port: 65432,
})


console.log('connecting...')
client.connect()

// callback
console.log('querying...')
// client.query('SELECT NOW() as now', (err, res) => {
//   if (err) {
//     console.log(err.stack)
//   } else {
//     console.log(res.rows[0])
//   }:q })
//

client.query('SELECT NOW() as now', (err, res) => {
  if (err) {
    console.log(err.stack)
  } else {
    console.log(res.rows[0])
  }
})

// promise

