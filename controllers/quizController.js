const User = require('../models/User')
const Quiz = require('../models/Quiz')
const asyncHandler = require('express-async-handler')

//don't add route protection to this route
//description : Get all quizzes
//route : GET /quiz/organization
//access : private
const getAllQuizzes = asyncHandler(async (req,res) => {
    // const { organization } = req.body

    //get all quizzes
    const quizzes = await Quiz.find().lean()
    console.log(quizzes)

    // // filter quizzes from users in the same organization
    // const quizzes = await Quiz.find({})
    // .populate({
    //     path: 'user',
    //     match: {'organization': organization }
    // })
    // .exec();

    // // Now, you can filter the quizzes based on the populated user field
    // const filteredQuizzes = quizzes.find(quiz => quiz.user !== null);

    // res.json(filteredQuizzes)

    if(!quizzes?.length) {
        return res.status(400).json({ message: 'No quizzes found'})
    }

    // quizszes with owner's usernames
    const quizzesWithOwner = await Promise.all(quizzes.map(async (quiz) => {
        const user = await User.findById(quiz.user).lean().exec()
        return { ...quiz, username: user.username }
    }))

    res.json(quizzesWithOwner)

})

//description : Get all quizzes of a single user
//route : GET /quiz/:userID
//access : private
const getUserQuizzes = asyncHandler(async (req,res) => {
    const { userId } = req.params

    // const user = await User.findById(userId).lean().exec()
    //get all quizzes
    const quizzes = await Quiz.find({ user: userId }).exec();

    if(!quizzes?.length) {
        return res.status(400).json({ message: 'No quizzes found'})
    }

    res.json(quizzes)

})


//description : Add quiz
//route : POST /quiz
//access : private

const createQuiz = asyncHandler(async (req, res) => {
    const { user, course_code, title, guidelines, questions } = req.body

    var { start_time, end_time } = req.body
    start_time = new Date(start_time)
    end_time = new Date(end_time )

    if (!user || !course_code || !title || !guidelines || !start_time || !end_time) {
        return res.status(400).json({ message: 'All fields required'})
    }

    //check if quiz already exists for the course at the given time period
    const quizExists = await Quiz.findOne({
        $and: [{ "start_time": {"$lt": end_time}, "end_time": {"$gt": start_time} }, { "course_code": course_code } ]
    })
    
    if(quizExists) {
        console.log(quizExists)
        return res.status(400).json({message: 'Quiz already exist!'})
    }

    // console.log("validation success")

    // Create quiz
    const quiz = await Quiz.create({
        user,
        course_code,
        title,
        guidelines,
        start_time,
        end_time,
        questions
    })

    // console.log("create success")

    //response
    if (quiz) {
        res.status(201).json({
        message: `Quiz created successfully!`,    
        _id: quiz.id,
        course_code: quiz.course_code,
        title: quiz.title,
        guidelines: quiz.guidelines,
        start_time: quiz.start_time,
        end_time: quiz.end_time,
        questions: quiz.questions
        })
    } else {
        res.status(400).json({ message: 'Invalid quiz data!'})
    }

})


//description : Update quiz
//route : PUT /quiz
//access : private

const updateQuiz = asyncHandler(async (req, res) => {
    const { id, course_code, title, guidelines, start_time, end_time, questions, completed } = req.body

    if (!id || !course_code || !title || !guidelines || !start_time || !end_time|| typeof completed !== 'boolean') {
        return res.status(400).json({ message: 'All fields required'})
    }

    const quiz = await Quiz.findById(id).exec()

    if (!quiz) {
        return res.status(400).json({ message: 'Quiz not found!'})
    }

    //check if user is trying to update a completed quiz and deny updating


    //check if quiz already exists for the course at the given time period
    const quizExists = await Quiz.findOne({
        $and: [{ "start_time": {"$lt": end_time}, "end_time": {"$gt": start_time} }, { "course_code": course_code } ]
    })
    
    if(quizExists && quizExists?._id.toString() !== id) {
        console.log(quizExists)
        return res.status(400).json({message: 'Quiz already exist!'})
    }

    quiz.course_code = course_code
    quiz.title = title
    quiz.guidelines = guidelines
    quiz.start_time = start_time
    quiz.end_time = end_time
    quiz.completed = completed

    await quiz.save()

    res.json({ message: 'Quiz updated successfully'})
})

//description : Delete user
//route : DELETE /users
//access : private

const deleteQuiz = asyncHandler(async (req, res) => {
    const { id } = req.body

    if (!id) {
        return res.status(400).json({ message: 'Quiz ID required' })
    }

    const quiz = await Quiz.findById(id).exec()

    if(!quiz) {
        return res.status(400).json({ message: 'Quiz not found' })
    }

    const result = await quiz.deleteOne()

    const reply = `Quiz ${result.title} with ID ${result._id} deleted`

    res.json(reply)

})

module.exports = {
    getAllQuizzes,
    getUserQuizzes,
    createQuiz,
    updateQuiz,
    deleteQuiz
}
