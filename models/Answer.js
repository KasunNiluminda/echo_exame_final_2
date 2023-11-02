const mongoose = require('mongoose')

const questionAnswerSchema = new mongoose.Schema(
    {
        questionId: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'Question'
        },
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'User'
        },
        answer: {
            type: String,
            default: '',
            required: false
        },
        options: { 
            type: Array, 
            required: false 
        },
        correct: {
            type: Boolean,
            required: false
        }
    },
    {
        timestamps: true
    }
)

// Add a unique compound index on questionId and userId to prevent duplicates
questionAnswerSchema.index({ questionId: 1, userId: 1 }, { unique: true });

const questionAnswer = mongoose.model('QuestionAnswer', questionAnswerSchema)

const quizAnswerSchema = new mongoose.Schema(
    {
        quizId: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'Quiz'
        },
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'User'
        },
        //include correct answer and if correct and marks(if correct)
        answers: [
            {
                type: mongoose.Schema.Types.ObjectId,
                required: false,
                ref: 'QuestionAnswer'
            },
        ],
        totalMarks: {
            type: Number,
            default: 0,
            required: true,
        }
    },
    {
        timestamps: true
    }
)

const quizAnswer = mongoose.model('QuizAnswer', quizAnswerSchema)

module.exports = {
    questionAnswer,
    quizAnswer
} 