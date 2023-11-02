const express = require('express');
const router = express.Router();
const audioController = require('../controllers/audioController');
const voiceController = require("../controllers/voiceController");

router.post("/identify-voice", voiceController.identifyVoice);
router.post('/user_identifier', audioController.uploadMiddleware, audioController.uploadAudio);
// router.get('/runPythonScript', audioController.runPythonScript); // Add the new route

module.exports = router;
