const User = require('../models/User')
const Quiz = require('../models/Quiz')
const Question = require('../models/Question')
const asyncHandler = require('express-async-handler')

//add route protection to this route
//description : Get all questions
//route : GET /question
//access : private
const getAllQuestions = asyncHandler(async (req,res) => {
    //get all questions
    const questions = await Question.find().lean()

    if(!questions?.length) {
        return res.status(400).json({ message: 'No questions found'})
    }
    // console.log(questions)

    // const quiz = await Quiz.find({questions : '65207e129c4ca601e9ebed2a'}).lean().exec()
    // console.log(quiz)

    // questions with quiz title


    const questionsWithQuiz = await Promise.all(questions.map(async (question) => {
        const quiz = await Quiz.findOne({ questions: question._id.toString() }).lean().exec();
        
        // console.log(quiz)

        // Check if a quiz was found for the question
        if (quiz) {
            return { ...question, title: quiz.title };
        } else {
            // Handle the case where no quiz was found (you can decide what to do)
            return { error: "No Quiz allocated", ...question };
        }
    }));
    

    res.json(questionsWithQuiz)
    // res.json(questions)

})

//description : Get all questions of a quiz
//route : GET /question/:quizId
//access : private
const getQuizQuestions = asyncHandler(async (req,res) => {
    const { quizId } = req.params

    // const user = await User.findById(userId).lean().exec()
    //get all quizzes
    // const quiz = await Quiz.find({ _id: quizId }).exec();
    const questionIds = await Quiz.findOne({ _id: quizId },{questions:1}).exec();

    // console.log(questionIds.questions)

    if(questionIds.questions.length == 0) {
        return res.status(400).json({ message: 'No questions found'})
    }

    const quizQuestions = await Promise.all(questionIds.questions.map(async (questionId) => {
        const question = await Question.findOne({ _id : questionId }).lean().exec();
        
        //  console.log(question)

        // Check if a quiz was found for the question
        if (question) {
            return { questionId: questionId, question: question.question, quizId: quizId };
        } else {
            // Handle the case where no quiz was found (you can decide what to do)
            return { error: "Question Not Found", ...question };
        }
    }));

    res.json(quizQuestions)

})


//description : Add question
//route : POST /question
//access : private

const addQuestion = asyncHandler(async (req, res) => {
    const { quizId, question, questionType, options, correctOptions, answer, marks } = req.body

    if (!quizId || !question || !questionType || !marks) {
        return res.status(400).json({ message: 'All fields required'})
    }

    if (questionType == "MCQ") {
        if(!options || !correctOptions) {
            return res.status(400).json({ message: 'Options and correct options required for a MCQ'})
        }

        
    }

    if (questionType == "Short Answer") {
        if(!answer) {
            return res.status(400).json({ message: 'Answer required for a Short answer question'})
        }

        
    }

    // // Check if question already exists in the quiz
    // const questionExists = await Question.findOne({ question: question });

    // if (questionExists) {
    //     const quizOfQuestion = await Quiz.findOne({ questions: questionExists._id });

    //     if (quizOfQuestion._id.toString() === quizId) {
    //         console.log(questionExists);
    //         return res.status(400).json({ message: 'Question already exists in the quiz!' });
    //     }
    // }


    //can check if number of questions exceeded if needed

    
    console.log("validation success")

    

    // Create quiz
    const questionCreated = await Question.create({
        quizId,
        question,
        questionType,
        options,
        correctOptions,
        answer,
        marks
    })

    // console.log("create success")


    //response
    if (questionCreated) {
        Quiz.findByIdAndUpdate(quizId, {
            $push: { questions:{"_id" : questionCreated.id} }
          })
            .then((result) => {
              if (!result) {
                // The quiz with the given ID was not found.
                console.log('Quiz not found.');
              } else {
                console.log('Question added to quiz successfully.');
              }
            })
            .catch((error) => {
              console.error('Error:', error);
            });
          

        res.status(201).json({
        message: `Question added successfully!`,    
        _id: questionCreated.id,
        quizId:questionCreated.quizId,
        question:questionCreated.question,
        questionType:questionCreated.questionType,
        options:questionCreated.options,
        correctOptions:questionCreated.correctOptions,
        answer:questionCreated.answer,
        marks:questionCreated.marks        
        })
    } else {
        res.status(400).json({ message: 'Invalid question data!'})
    }

})


//description : Update question
//route : PUT /question
//access : private

const updateQuestion = asyncHandler(async (req, res) => {
    const { quizId, questionId, question, questionType, marks } = req.body
    var { options, correctOptions, answer } =req.body

    if (!questionId || !quizId || !question || !questionType || !marks) {
        return res.status(400).json({ message: 'All fields required'})
    }

    const questionExists = await Question.findById(questionId).exec()

    if (questionExists?.questionType !== questionType) {
        if (questionType == "MCQ") {

            //remove answer if questionType changed to MCQ
            if(questionExists?.answer !== null)
                answer = ""

            if(!options || !correctOptions) {
                return res.status(400).json({ message: 'Options and correct options required for a MCQ'})
            }
            
        }
    
        if (questionType == "Short Answer") {

            //remove options and correct options if questionType changed to ShortAnswer
            if(questionExists?.options.length !== 0){
                options = []
                correctOptions = []
            }

            if(!answer) {
                return res.status(400).json({ message: 'Answer required for a Short answer question'})
            }
            
        }
    }

    // // Check if question already exists in the quiz
    // const questionExists = await Question.findOne({ question: question });

    // if (questionExists) {
    //     const quizOfQuestion = await Quiz.findOne({ questions: questionExists._id });

    //     if (quizOfQuestion._id.toString() === quizId) {
    //         console.log(questionExists);
    //         return res.status(400).json({ message: 'Question already exists in the quiz!' });
    //     }
    // }


    //can check if number of questions exceeded if needed

    
    console.log("validation success")

    
    questionExists.question = question
    questionExists.questionType = questionType
    questionExists.options = options
    questionExists.correctOptions = correctOptions
    questionExists.answer = answer
    questionExists.marks = marks

    await questionExists.save()

    res.json({ message: 'Question updated successfully'})

})

//description : Delete question
//route : DELETE /question
//access : private

const deleteQuestion = asyncHandler(async (req, res) => {
    const { quizId, questionId } = req.body

    if (!questionId || !quizId) {
        return res.status(400).json({ message: 'Question ID and Quiz ID required' })
    }

    const question = await Question.findById(questionId).exec()

    if(!question) {
        return res.status(400).json({ message: 'Question not found' })
    }


    Quiz.findByIdAndUpdate(quizId, {
        $pull: { questions: questionId }
      })
        .then((result) => {
          if (!result) {
            // The quiz with the given ID was not found.
            console.log('Quiz not found.');
          } else {
            console.log('Question added to quiz successfully.');
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
        
    const result = await question.deleteOne()

    const reply = `Question '${result.question}' with ID ${result._id} deleted`

    res.json(reply)

})


module.exports = {
    getAllQuestions,
    getQuizQuestions,
    addQuestion,
    updateQuestion,
    deleteQuestion
}






