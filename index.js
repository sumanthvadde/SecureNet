const express = require('express');
const user = require('./src/route/userroute');
const app = express();
app.use(express.json());
app.use(user);
const port = process.env.PORT || 3000;

app.listen(port, console.log(`Server started on ${port}`));