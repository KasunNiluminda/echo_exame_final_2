const { spawn } = require("child_process");

// Define the Python script path and command line arguments
const pythonScript = "pythonModels/voice_to_text/voiceToText.py";

const voiceToVoiceCheck = async (req, res) => {
  const audioFilePath = req.body.audioFilePath; // Get image data from the request

  // Call the Python script using child process
  const pythonProcess = spawn("python", [pythonScript, audioFilePath]);

  let recognizedText = "";

  pythonProcess.stdout.on("data", (data) => {
    recognizedText += data.toString();
  });

  pythonProcess.on("close", (code) => {
    if (code === 0) {
      resolve(recognizedText.trim());
    } else {
      reject(new Error(`Python script exited with code ${code}`));
    }
  });
};

module.exports = {
  voiceToVoiceCheck,
};
