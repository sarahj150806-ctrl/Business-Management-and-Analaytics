const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

const SECRET = "free_analytics_secret_key";
const db = new sqlite3.Database('./users.db');

db.run(`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT)`);

app.post('/api/signup', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: "Missing required fields." });

  const hashedPassword = await bcrypt.hash(password, 10);
  
  db.run(`INSERT INTO users (email, password) VALUES (?, ?)`, [email, hashedPassword], function(err) {
    if (err) return res.status(400).json({ error: "User already exists." });
    res.json({ message: "User created successfully." });
  });
});

app.post('/api/login', (req, res) => {
  const { email, password } = req.body;
  db.get(`SELECT * FROM users WHERE email = ?`, [email], async (err, user) => {
    if (err || !user) return res.status(400).json({ error: "Invalid credentials." });
    
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) return res.status(400).json({ error: "Invalid credentials." });

    const token = jwt.sign({ id: user.id, email: user.email }, SECRET, { expiresIn: '2h' });
    res.json({ token });
  });
});

app.listen(5000, () => console.log('Node.js Auth API online at http://localhost:5000'));