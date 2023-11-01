const express = require('express')
const router = express.Router()
const {
    getAllQuizzes,
    getUserQuizzes,
    createQuiz,
    updateQuiz,
    deleteQuiz,
} = require('../controllers/quizController')

router.route('/')
    .get(getAllQuizzes)
    .post(createQuiz)
    .patch(updateQuiz)
    .delete(deleteQuiz)

router.route('/:userId').get(getUserQuizzes)

module.exports = router