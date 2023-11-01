const { spawn } = require("child_process");

const runPythonScript = () => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python", [
      "pythonModels/identify/identify3.py",
    ]);

    let pythonOutput = ""; // Store Python script output
    
    pythonProcess.stdout.on("data", (data) => {
      pythonOutput += data.toString(); // Collect the output
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python stderr: ${data}`);
    });

    pythonProcess.on("error", (error) => {
      reject(error);
    });

    pythonProcess.on("close", (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(pythonOutput);
          resolve(result);
        } catch (error) {
          reject("Failed to parse Python script output as JSON.");
        }
      } else {
        reject(`Python script execution failed with code ${code}`);
      }
    });
  });
};

module.exports = {
  identifyVoice: async (req, res) => {
    try {
      const result = await runPythonScript();
      res.json(result);
    } catch (error) {
      res.json({ error: error });
    }
  },
};

// const { spawn } = require("child_process");

// const runPythonScript = () => {
//   return new Promise((resolve, reject) => {
//     const pythonProcess = spawn("python", [
//       "src/pythonModels/identify/identify3.py",
//     ]);
//     // console.log(audioFilePath);
//     pythonProcess.stdout.on("data", (data) => {
//       try {

//         const result = JSON.parse(data.toString());
//         resolve(result);
//       } catch (error) {
//         console.error(`Python stderr: ${data}`);
//         reject(error);
//       }
//     });

//     pythonProcess.on("error", (error) => {
//       reject(error);
//     });
//   });
// };

// module.exports = {
//   identifyVoice: async (req, res) => {
//     try {
//       const result = await runPythonScript();
//       res.json(result);
//     } catch (error) {
//       res.status(500).json({ error: "An error occurred" });
//     }
//   },
// };
