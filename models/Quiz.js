const mongoose = require('mongoose')
const AutoIncrement = require('mongoose-sequence')(mongoose)

const quizSchema = new mongoose.Schema(
    {
        user: {
            type: mongoose.Schema.Types.ObjectId,
            required: true,
            ref: 'User'
        },
        course_code: {
            type: String,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        guidelines: {
            type: String,
            required: true
        },
        start_time: {
            type: Date,
            required: true
        },
        end_time: {
            type: Date,
            required: true
        },
        questions: [
            {
              type: mongoose.Schema.Types.ObjectId,
              ref: 'Question'
            }
          ],
        completed: {
            type: Boolean,
            default: false
        }
    },
    {
        timestamps: true
    }
)

// quizSchema.plugin(AutoIncrement, {
//     inc_field: 'quizno',
//     id: 'quizNo',
//     start_seq: 100
// })

module.exports = mongoose.model('Quiz', quizSchema)