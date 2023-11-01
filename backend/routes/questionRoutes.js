const express = require('express')
const router = express.Router()
const {
    getAllQuestions,
    getQuizQuestions,
    addQuestion,
    updateQuestion,
    deleteQuestion
} = require('../controllers/questionController')

router.route('/')
    .get(getAllQuestions)
    .post(addQuestion)
    .patch(updateQuestion)
    .delete(deleteQuestion)

router.route('/:quizId').get(getQuizQuestions)

module.exports = router