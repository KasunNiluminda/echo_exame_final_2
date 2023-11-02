require('dotenv').config()
const express = require('express')
const app = express()
const path = require('path')
const errorHandler = require('./middleware/errorHandler')
const cookieParser = require('cookie-parser')
const cors = require('cors')
const corsOptions = require('./config/corsOptions')
const connectDB = require('./config/dbConn')
const mongoose = require('mongoose')
const { logger, logEvents } = require('./middleware/logger')
const PORT = process.env.PORT || 3500


const user_identifier = require('./routes/user_identifierRoutes');
const user_intensity = require('./routes/user_intensity');
const face_ditectoin = require('./routes/face_ditectoin');
const voice_to_voice = require('./routes/voice_to_voice');

// console.log(process.env.NODE_ENV)

connectDB()

app.use(logger)

app.use(cors(corsOptions))
// app.use(cors())

app.use(express.json())

app.use(cookieParser())

app.use('/', express.static(path.join(__dirname, 'public')))

app.use('/', require('./routes/root'))
app.use('/users', require('./routes/userRoutes'))
app.use('/quiz', require('./routes/quizRoutes'))
app.use('/question', require('./routes/questionRoutes'))
app.use('/answer', require('./routes/answerRoutes'))


//------------------- python models------------------------------------------
app.use('/api/student', user_identifier);

app.use('/api/student', user_intensity);

app.use('/api/student', face_ditectoin);

app.use('/api/student', voice_to_voice);



app.all('*', (req, res) => {
    res.status(404)
    if (req.accepts('html')) {
        res.sendFile(path.join(__dirname, 'views', '404.html'))
    } else if (req.accepts('json')) {
        res.json({ message: '404 Not Found' })
    } else {
        res.type('txt').send('404 Not Found')
    }
})

app.use(errorHandler)

mongoose.connection.once('open', () => {
    console.log('Connected to MongoDB')
    app.listen(PORT, () => console.log(`Server running on port ${PORT}`))
})

mongoose.connection.on('error', err => {
    console.log(err)
    logEvents(`${err.no}: ${err.code}\t${err.syscall}\t${err.hostname}`,
    'mongoErrLog.log')
})