const { spawn } = require("child_process");

// Define the Python script path and command line arguments
const pythonScript = "src/pythonModels/face_ditection/faceDitection.py";

const detect_face = async (req, res) => {
  const imageData = req.body.imageData; // Get image data from the request

  // Call the Python script using child process
  const pythonProcess = spawn("python", [pythonScript, imageData]);

  pythonProcess.stdout.on("data", (data) => {
    // Handle the output from the Python script if needed
    console.log(`Python script output: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    res.send("Image processed successfully");
  });
};

module.exports = {
  detect_face,
};
