const { Pool, Client } = require('pg')

const client = new Client({
  user: 'explorer',
  host: 'tofu.gps.caltech.edu',
  database: 'spatial_db',
  password: 'secretpassword',
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
//   }
// })
// promise
client
  .query('SELECT NOW() as now')
  .then(res => console.log(res.rows[0]))
  .catch(e => console.error(e.stack))

client.end()