const mongoose = require('mongoose')

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    organization: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    //set default user to student
    role: {
        type: String,
        enum: ['Student', 'Lecturer', 'Admin'],
        default: "Student"
    },
    //To remove user access
    active: {
        type: Boolean,
        default: true
    }
})

module.exports = mongoose.model('User', userSchema)