const mongoose = require('mongoose')

const questionSchema = new mongoose.Schema(
    {
        quizId: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'Quiz'
        },
        question: {
            type: String,
            required: true
        },
        questionType: { 
            type: String,
            enum: ['MCQ', 'Short Answer'],
            required: true 
        },
        options: { 
            type: Array, 
            required: false 
        },
        correctOptions: { 
            type: Array, 
            required: false
        },
        answer:{
            type: String, 
            required: false 
        },
        marks: { 
            type: Number, 
            required: true 
        }
    },
    {
        timestamps: true
    }
)

module.exports = mongoose.model('Question', questionSchema)