const express = require('express')
const router = express.Router()
const {
    getAllAnswers,
    getUserQuestionAnswers,
    getUserQuizAnswers,
    getQuizQuestionAnswers,
    addAnswer,
    addQuizAnswers,
    // updateAnswer,
    // deleteAnswer
} = require('../controllers/answerController')

router.route('/')
    .get(getAllAnswers)
    .post(addAnswer)
    // .patch(updateAnswer)
    // .delete(deleteAnswer)

router.route('/quizAnswer').post(addQuizAnswers)
router.route('/userQuestion').get(getUserQuestionAnswers)
router.route('/userQuiz').get(getUserQuizAnswers)
router.route('/quizQuestion').get(getQuizQuestionAnswers)

module.exports = router