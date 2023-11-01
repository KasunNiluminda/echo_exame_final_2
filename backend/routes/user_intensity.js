const express = require('express');
const router = express.Router();
const intensityController = require('../controllers/intensityController');
const intensityCheckController = require("../controllers/intensityCheckController");

router.post("/intensity_check", intensityCheckController.intensity_check);
router.post('/user_intensity', intensityController.uploadMiddleware, intensityController.uploadAudio);
// router.get('/runPythonScript', audioController.runPythonScript); // Add the new route

module.exports = router;
