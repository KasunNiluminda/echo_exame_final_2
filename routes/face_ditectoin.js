const express = require('express');
const router = express.Router();
const faceDitectoinController = require('../controllers/faceDitectoinController');

router.post('/face_ditectoin', faceDitectoinController.detect_face);


module.exports = router;
