const express = require('express');
const router = express.Router();
const voiceToVoiceController = require('../controllers/voiceToVoiceController');

router.post('/voice_to_voice', voiceToVoiceController.voiceToVoiceCheck);


module.exports = router;
