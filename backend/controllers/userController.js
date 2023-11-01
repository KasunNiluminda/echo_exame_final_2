const User = require('../models/User')
const Quiz = require('../models/Quiz')
const asyncHandler = require('express-async-handler')
const jwt = require('jsonwebtoken')
const bcrypt = require('bcrypt')

//description : Get all users
//route : GET /users
//access : private

const getAllUsers = asyncHandler(async (req, res) => {
    const users = await User.find().select('-password').lean()
    
    if(!users?.length) {
        return res.status(400).json({message: 'No users found'})
    }
    res.json(users)
})

//description : Add user
//route : POST /users
//access : private

const createUser = asyncHandler(async (req, res) => {
    const { username, email, organization, password, role } = req.body

    if (!username || !email || !organization || !password || !role) {
        return res.status(400).json({message: 'All fields required'})
    }

    //check if user already exists
    const userExists = await User.findOne({ email }).lean().exec()

    if(userExists && userExists?.organization == organization) {
        return res.status(400).json({message: 'User already exist!'})
    }

      // Hash password
    const salt = await bcrypt.genSalt(10)
    const hashedPassword = await bcrypt.hash(password, salt)

    // Create user
  const user = await User.create({
    username,
    organization,
    email,
    role,
    password: hashedPassword,
  })

  if (user) {
    res.status(201).json({
    message: `User created successfully!`,    
    _id: user.id,
    username: user.username,
    organization: user.organization,
    email: user.email,
    role: user.role,
    token: generateToken(user.id),
    })
  } else {
    res.status(400).json({ message: 'Invalid user data!'})
  }

})

//description : Update user
//route : PUT /users
//access : private

const updateUser = asyncHandler(async (req, res) => {
    const { id, username, organization, email, role, password, active } = req.body

    // if (!id || !username || !organization || !email || !role || typeof active !== 'boolean') {
    //     return res.status(400).json({ message: 'All fields required'})
    // }

    const user = await User.findById(id).exec()

    if (!user) {
        return res.status(400).json({ message: 'User not found!'})
    }

    // //check if user is trying to update email to an existing email
    // const duplicateEmail = await User.findOne({ email }).lean().exec()

    // //same user with same email can be in 2 organizationa
    // if (duplicateEmail && duplicateEmail?._id.toString() !== id && duplicateEmail?.organization == organization) {
    //     return res.status(409).json({ message: 'Another user exist with this email exist in the organization'})
    // }

    user.username = username

    //password and email reset with SMTP

    await user.save()

    res.json({ message: 'user updated successfully'})
})

//description : Delete user
//route : DELETE /users
//access : private

const deleteUser = asyncHandler(async (req, res) => {
    const { id } = req.body

    if (!id) {
        return res.status(400).json({ message: 'User ID required' })
    }

    const user = await User.findById(id).exec()

    if(!user) {
        return res.status(400).json({ message: 'User not found' })
    }

    const result = await user.deleteOne()

    const reply = `Username ${result.username} with ID ${result._id} deleted`

    res.json(reply)

})

// Generate JWT
const generateToken = (id) => {
    return jwt.sign({ id }, process.env.JWT_SECRET, {
      expiresIn: '30d',
    })
  }

module.exports = {
    getAllUsers,
    createUser,
    updateUser,
    deleteUser
}
