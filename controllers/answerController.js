const User = require('../models/User')
const { questionAnswer, quizAnswer } = require('../models/Answer')
const Question = require('../models/Question')
const asyncHandler = require('express-async-handler')

//add route protection to this route
//description : Get all answers with question
//route : GET /answer
//access : private
const getAllAnswers = asyncHandler(async (req,res) => {
    //get all answers
    const answers = await questionAnswer.find().lean()

    if(!answers?.length) {
        return res.status(400).json({ message: 'No answers found'})
    }

    // answers with quiz title
    const answerWithQuestion = await Promise.all(answers.map(async (answer) => {
        const question = await Question.findById(answer.questionId).lean().exec()
        return { question : question.question, ...answer }
    }))

    res.json(answerWithQuestion )

})


//description : Get answer for a question by a user
//route : GET /answer/userQuestion
//access : private
const getUserQuestionAnswers = asyncHandler(async (req,res) => {
    const { answerId, userId } = req.body

    const user = await User.findById(userId).lean().exec()

    const answer = await questionAnswer.findOne({ _id : answerId }).exec();



    if(!user && answer.userId !== userId) {
        return res.status(400).json({ message: 'Answer of user not found'})
    }

    res.json({username:user.username , answer})

})

//description : Get answers from a user to a quiz
//route : GET /answer/userQuiz
//access : private


///////////////// DELETE /////////////////////
// const getUserQuizAnswers = asyncHandler(async (req,res) => {
//     const { userId, quizId } = req.body

//     const user = await User.findById(userId).lean().exec()
//     //get all quizzes
//     const quizans = await quizAnswer.findOne({quizId}).exec();

//     console.log(quizans)

//     if(!user && quizans.userId !== userId) {
//         return res.status(400).json({ message: 'Quiz answers of user not found'})
//     }

//     // const answers = await questionAnswer.find({'quiz.answers': {$elemMatch: {id : quizId}}})
//     const answers = await questionAnswer.find({ _id: quizans.id },{answers:1})

//     res.json(answers)

// })
//////////////////////////////////////////////

const getUserQuizAnswers = asyncHandler(async (req, res) => {
    const { userId, quizId } = req.body; // Assuming these values come from URL parameters
  
    const user = await User.findById(userId).lean().exec();
    const quizAnswers = await quizAnswer.find({ quizId, userId }).lean().exec();
  
    // console.log(user)
    // console.log(quizAnswers)

    if (!user || quizAnswers.length === 0) {
      return res.status(400).json({ message: 'User or quiz answers not found' });
    }

    if (quizAnswers.length > 1) {
      return res.status(400).json({ message: 'Error! Duplicate answers found' });
    }

    const answerIds = quizAnswers[0].answers; // Assuming you want to access answers from the first quizAnswer document
  
    // Fetch question answers based on answerIds
    const answers = await questionAnswer.find({ _id: { $in: answerIds } }).lean().exec();
  
    res.json(answers);
  });
  

//description : Get all answers for a question
//route : GET /answer/quizQuestion
//access : private


// const getQuizQuestionAnswers = asyncHandler(async (req,res) => {
//     const { questionId } = req.body

    
//     // const quiz = await Quiz.find({ _id: quizId }).exec();
//     const answers = await questionAnswer.find({ questionId : questionId }).exec();

//     if(!answers?.length) {
//         return res.status(400).json({ message: 'No answers found'})
//     }

//     res.json(answers)

// })


const getQuizQuestionAnswers = asyncHandler(async (req, res) => {
    const { questionId } = req.body;
  
    try {
      const answers = await questionAnswer.find({ questionId: questionId }).exec();
  
      if (!answers?.length) {
        return res.status(400).json({ message: 'No answers found' });
      }
  
      res.json(answers);
    } catch (error) {
        // ERROR not working

      // Check if the error is due to a duplicate key violation (duplicate answer for the same user and question)
      if (error.code === 11000) {
        return res.status(400).json({ message: 'Duplicate answer for the same user and question' });
      }
  
      // Handle other errors
      console.error(error);
      res.status(500).json({ message: 'Internal server error' });
    }
  });

  

//description : Add quiz answer
//route : POST /answer/quizAnswer
//access : private

const addQuizAnswers = asyncHandler(async (req, res) => {
    const { quizId, userId } = req.body

    if (!quizId || !userId) {
        return res.status(400).json({ message: 'All fields required'})
    }

    const quizAnswers = await quizAnswer.findOne({$and:[{quizId : quizId},{userId: userId}]}).exec();

    if(quizAnswers) {
        return res.status(400).json({ message: 'quiz already attempted' })
    }

    const quizAnswersCreated = await quizAnswer.create({
        quizId,
        userId,
        answers:[]
    })

    // console.log("create success")


    //response
    if (quizAnswersCreated) {
        
        res.status(201).json(quizAnswersCreated)
    } else {
        res.status(400).json({ message: 'Invalid data!'})
    }

})

//description : Add answer
//route : POST /answer
//access : private

const addAnswer = asyncHandler(async (req, res) => {
    const { questionId, quizId, userId, answer, options } = req.body

    if (!questionId || !quizId || !userId) {
        return res.status(400).json({ message: 'All fields required'})
    }

    if ( !answer && !options ) {
        return res.status(400).json({ message: 'Not answered' })
    }

    const question = await Question.findById(questionId).exec();

    var correct = false

    if (answer) {
        if(answer.toLowerCase() == question.answer.toLocaleLowerCase()) {
            correct = true
        }
    }

    if (options) {

        ///////////////////// NOT WORKING ////////////////////

        //compare all options in the array
        if(options == question.correctOptions) {
            correct = true

            //calculate marks according to number of correct options
            //address weignhted answers
        }  
    }

    console.log(correct)

    // Create quiz
    const answerCreated = await questionAnswer.create({
        questionId,
        userId,
        answer,
        options,
        correct
    })

    // console.log("create success")

    const quizAnswerExists = await quizAnswer.findOne({$and: [{ quizId: quizId },{ userId: userId }]}).exec();

    if (!quizAnswerExists) {
        return res.status(400).json({ message: 'Not attempted' })
    }

    console.log(quizAnswerExists)

    //response
    if (answerCreated) {
        quizAnswer.findOneAndUpdate(
            { quizId, userId },
            { $push: { answers: answerCreated.id } },
            { new: true } // This option returns the updated document
          )
            .then((updatedQuizAnswer) => {
              if (!updatedQuizAnswer) {
                console.log('Quiz answer not found.'); // No matching document was found
                return res.status(404).json({ message: 'Quiz answer not found.' });
              }
          
              console.log('Answer added successfully.');
              // You can send a success response or handle it as needed
              // return res.status(200).json(updatedQuizAnswer);
              return
            })
            .catch((error) => {
              console.error('Error:', error);
              return res.status(500).json({ message: 'Internal Server Error' }); // Handle the error with an appropriate response
            });
          

        res.status(201).json({
        message: `Answer added successfully!`,    
        _id: answerCreated.id,
        questionId:answerCreated.questionId,
        userId:answerCreated.userId,
        answer:answerCreated.answer,
        options:answerCreated.options,      
        })
    } else {
        res.status(400).json({ message: 'Invalid question data!'})
    }

})


// //description : Update question
// //route : PUT /question
// //access : private

// const updateQuestion = asyncHandler(async (req, res) => {
//     const { quizId, questionId, question, questionType, marks } = req.body
//     var { options, correctOptions, answer } =req.body

//     if (!questionId || !quizId || !question || !questionType || !marks) {
//         return res.status(400).json({ message: 'All fields required'})
//     }

//     const questionExists = await Question.findById(questionId).exec()

//     if (questionExists?.questionType !== questionType) {
//         if (questionType == "MCQ") {

//             //remove answer if questionType changed to MCQ
//             if(questionExists?.answer !== null)
//                 answer = ""

//             if(!options || !correctOptions) {
//                 return res.status(400).json({ message: 'Options and correct options required for a MCQ'})
//             }
            
//         }
    
//         if (questionType == "Short Answer") {

//             //remove options and correct options if questionType changed to ShortAnswer
//             if(questionExists?.options.length !== 0){
//                 options = []
//                 correctOptions = []
//             }

//             if(!answer) {
//                 return res.status(400).json({ message: 'Answer required for a Short answer question'})
//             }
            
//         }
//     }

//     // // Check if question already exists in the quiz
//     // const questionExists = await Question.findOne({ question: question });

//     // if (questionExists) {
//     //     const quizOfQuestion = await Quiz.findOne({ questions: questionExists._id });

//     //     if (quizOfQuestion._id.toString() === quizId) {
//     //         console.log(questionExists);
//     //         return res.status(400).json({ message: 'Question already exists in the quiz!' });
//     //     }
//     // }


//     //can check if number of questions exceeded if needed

    
//     console.log("validation success")

    
//     questionExists.question = question
//     questionExists.questionType = questionType
//     questionExists.options = options
//     questionExists.correctOptions = correctOptions
//     questionExists.answer = answer
//     questionExists.marks = marks

//     await questionExists.save()

//     res.json({ message: 'Question updated successfully'})

// })

// //description : Delete answer
// //route : DELETE /answer
// //access : private

// const deleteAnswer = asyncHandler(async (req, res) => {
//     const { quizId, questionId, answerId } = req.body

//     if (!answerId || !quizId || !questionId) {
//         return res.status(400).json({ message: 'AnswerID, QuizID and QuestionID required' })
//     }

//     const answer = await questionAnswer.findById(answerId).exec()

//     if(!answer) {
//         return res.status(400).json({ message: 'Answer not found' })
//     }


//     QuizAnswer.findByIdAndUpdate(quizId, {
//         $pull: { answers: answerId }
//       })
//         .then((result) => {
//           if (!result) {
//             // The quiz with the given ID was not found.
//             console.log('Quiz not found.');
//           } else {
//             console.log('Answer added to quiz successfully.');
//           }
//         })
//         .catch((error) => {
//           console.error('Error:', error);
//         });
        
//     const result = await questionAnswer.deleteOne()

//     const reply = `Answer '${result.answer}' with ID ${result._id} deleted`

//     res.json(reply)

// })


module.exports = {
    getAllAnswers,
    getUserQuestionAnswers,
    getUserQuizAnswers,
    getQuizQuestionAnswers,
    addQuizAnswers,
    addAnswer,
    // updateAnswer,
    // deleteAnswer
}