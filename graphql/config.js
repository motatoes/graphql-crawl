const mongoose = require('mongoose');
mongoose.Promise = global.Promise;

const url = `mongodb://${process.env.MONGO_HOST}:${process.env.MONGO_PORT}`;

mongoose.connect(url, { 
    useNewUrlParser: true, 
    user: process.env.MONGO_USER,
    pass: process.env.MONGO_PASS,
    dbName: process.env.MONGO_DB    
});
mongoose.connection.once('open', () => console.log(`Connected to mongo at ${url}`));