const axios = require("axios");
const fileUpload = require("express-fileupload");
const fs = require("fs");
const path = require("path");

// Middleware for file uploads
const uploadMiddleware = fileUpload();

const uploadAudio = async (req, res) => {
  try {
    if (!req.files || !req.files.audio) {
      return res.status(400).json({ message: "No audio file uploaded" });
    }

    const audioData = req.files.audio;

    // Save the audio file to a directory
    const uploadDir = path.join(__dirname, "../pythonModels/intensity");
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }

    // Modify the file name to add ".wav" extension
    const fileName = `${audioData.name}.wav`;

    // Save the audio file with the modified file name
    const filePath = path.join(uploadDir, fileName);
    audioData.mv(filePath);

    // const filePath = path.join(uploadDir, audioData.name);
    // audioData.mv(filePath);

    // Now, make an HTTP POST request to the identify-voice endpoint
    // try {
    //   const response = await axios.post('http://localhost:3000/api/voice/identify-voice', {
    //     audioPath: filePath, // You might need to adjust the request data structure
    //   });

    const identifyVoiceUrl = `${process.env.BASE_URL}/student/intensity_check`;
    try {
      const response = await axios.post(identifyVoiceUrl, {
        audioPath: filePath,
      });

      // Handle the response from the POST request, e.g., return it to the client
      res.status(200).json({
        message: "Audio uploaded and processed successfully",
        response: response.data,
      });
    } catch (error) {
      console.error("Error making the POST request: ", error);
      res.status(500).json({ message: "Error making the POST request" });
    }
  } catch (error) {
    console.error("Error uploading audio: ", error);
    res.status(500).json({ message: "Error uploading audio" });
  }
};

module.exports = {
  uploadAudio,
  uploadMiddleware, // Export the middleware for use in your router
};





// const fileUpload = require("express-fileupload");
// const fs = require("fs");
// const path = require("path");
// const { exec } = require("child_process");

// // Middleware for file uploads
// const uploadMiddleware = fileUpload();

// const uploadAudio = async (req, res) => {
//   try {
//     if (!req.files || !req.files.audio) {
//       return res.status(400).json({ message: "No audio file uploaded" });
//     }

//     const audioData = req.files.audio;

//     const uploadDir = path.join(__dirname, "../pythonModels/identify");
//     if (!fs.existsSync(uploadDir)) {
//       fs.mkdirSync(uploadDir);
//     }
//     const filePath = path.join(uploadDir, audioData.name);
//     audioData.mv(filePath);

//     // Run the Python script and wait for the result
//     try {
//       const pythonResponse = await runPythonScript(filePath);
//       res
//         .status(200)
//         .json({ message: "Audio uploaded successfully", pythonResponse });
//     } catch (pythonError) {
//       console.error("Error running Python script: ", pythonError);
//       res.status(500).json({ message: "Error running Python script" });
//     }
//   } catch (error) {
//     console.error("Error uploading audio: ", error);
//     res.status(500).json({ message: "Error uploading audio" });
//   }
// };

// const runPythonScript = (req, res) => {
//   const pythonScriptPath = path.join(__dirname, "identify.py");
//   const voiceClip1Path = path.join(
//     __dirname,
//     "../pythonModels/1.wav",
//     req.files.audio.name
//   );
//   const voiceClip2Path = "../pythonModels/2.wav"; // Replace with the path to your second audio file

//   console.log("pythonScriptPath : ",pythonScriptPath);
//   console.log("voiceClip1Path : ",voiceClip1Path);
//   console.log("pythonScriptPath : ",voiceClip2Path);

//   // Command to run the Python script
//   const command = `python ${pythonScriptPath} ${voiceClip1Path} ${voiceClip2Path}`;

//   exec(command, (error, stdout, stderr) => {
//     if (error) {
//       console.error("Error running Python script: ", error);
//       res.status(500).json({ message: "Error running Python script" });
//     } else {
//       res.status(200).send(stdout);
//     }
//   });
// };

// module.exports = {
//   uploadAudio,
//   uploadMiddleware, // Export the middleware for use in your router
//   runPythonScript,
// };

// -------------
// const fileUpload = require("express-fileupload");
// const fs = require("fs");
// const path = require("path");
// const { spawn } = require("child_process");
// const { error } = require("console");

// // Middleware for file uploads
// const uploadMiddleware = fileUpload();

// const uploadAudio = (req, res) => {
//   try {
//     if (!req.files || !req.files.audio) {
//       return res.status(400).json({ message: "No audio file uploaded" });
//     }

//     const audioData = req.files.audio;

//     // Save the audio file to a directory
//     const uploadDir = path.join(__dirname, "../pythonModels/identify");
//     if (!fs.existsSync(uploadDir)) {
//       fs.mkdirSync(uploadDir);
//     }
//     const filePath = path.join(uploadDir, audioData.name);
//     audioData.mv(filePath);
//     // console.log(filePath);
//     const pythonScriptPath = " ";

//     // Execute the Python script for voice comparison
//     const pythonProcess = spawn("python", [pythonScriptPath]);

//     let scriptOutput = "";

//     pythonProcess.stdout.on("data", (data) => {
//       scriptOutput += data.toString();
//     });

//     pythonProcess.on("close", (code) => {
//       if (code === 0) {
//         // Python script executed successfully
//         res.status(200).json({
//           message: "Audio uploaded and processed",
//           output: scriptOutput,
//         });
//       } else {
//         console.error("Python script exited with an error.", error);
//         res.status(500).json({ message: "Error executing Python script" });
//       }
//     });
//   } catch (error) {
//     console.error("Error uploading audio: ", error);
//     res.status(500).json({ message: "Error uploading audio" });
//   }
// };

// module.exports = {
//   uploadAudio,
//   uploadMiddleware, // Export the middleware for use in your router
// };

// -------------

// const fileUpload = require("express-fileupload");
// const fs = require("fs");
// const path = require("path");
// const { spawn } = require("child_process");

// // Middleware for file uploads
// const uploadMiddleware = fileUpload();

// const uploadAudio = (req, res) => {
//   try {
//     if (!req.files || !req.files.audio) {
//       return res.status(400).json({ message: "No audio file uploaded" });
//     }

//     const audioData = req.files.audio;

//     // Save the audio file to a directory
//     const uploadDir = path.join(__dirname, "../pythonModels/identify");
//     if (!fs.existsSync(uploadDir)) {
//       fs.mkdirSync(uploadDir);
//     }
//     const filePath = path.join(uploadDir, audioData.name);
//     audioData.mv(filePath);
//     console.log(uploadDir);
//     console.log(filePath);
//     // Execute the Python script for voice comparison
//     const pythonProcess = spawn("python", ["identify.py", filePath]);

//     pythonProcess.on("error", (err) => {
//       console.error("Error executing Python script: ", err);
//       res.status(500).json({ message: "Error executing Python script" });
//     });

//     let scriptOutput = "";

//     pythonProcess.stdout.on("data", (data) => {
//       scriptOutput += data.toString();
//     });

//     pythonProcess.on("close", (code) => {
//       if (code === 0) {
//         // Python script executed successfully
//         res
//           .status(200)
//           .json({
//             message: "Audio uploaded and processed",
//             output: scriptOutput,
//           });
//       } else {
//         console.error("Python script exited with an error.");
//         res.status(500).json({ message: "Error executing Python script" });
//       }
//     });
//   } catch (error) {
//     console.error("Error uploading audio: ", error);
//     res.status(500).json({ message: "Error uploading audio" });
//   }
// };

// module.exports = {
//   uploadAudio,
//   uploadMiddleware, // Export the middleware for use in your router
// };

// corect base---------

// const fileUpload = require('express-fileupload');
// const fs = require('fs');
// const path = require('path');

// // Middleware for file uploads
// const uploadMiddleware = fileUpload();

// const uploadAudio = (req, res) => {
//   try {
//     if (!req.files || !req.files.audio) {
//       return res.status(400).json({ message: 'No audio file uploaded' });
//     }

//     // const audioData = req.files.audio;

//     // Save the audio file to a directory
//     const uploadDir = path.join(__dirname, '../pythonModels/identify');
//     if (!fs.existsSync(uploadDir)) {
//       fs.mkdirSync(uploadDir);
//     }
//     // const filePath = path.join(uploadDir, audioData.name);
//     // audioData.mv(filePath);

//     // Handle the audio data, e.g., save the file path to a database
//     // In a real application, you might want to store this in a database

//     res.status(200).json({ message: 'Audio uploaded successfully' });
//   } catch (error) {
//     console.error('Error uploading audio: ', error);
//     res.status(500).json({ message: 'Error uploading audio' });
//   }
// };

// module.exports = {
//   uploadAudio,
//   uploadMiddleware, // Export the middleware for use in your router
// };
