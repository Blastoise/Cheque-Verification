const path = require("path");
const { spawn } = require("child_process");
const express = require("express");
const bodyParser = require("body-parser");
const formidable = require("formidable");

const app = express();

// For parsing the req.body
app.use(bodyParser.urlencoded({ extended: false }));

// For Serving Files
app.use(express.static(`${__dirname}/public`));

app.get("/", (req, res) => {
  res.sendFile(`${__dirname}/public/index.html`);
});

app.post("/check", (req, res) => {
  // Array of arguments passed to the python file
  let arr = [path.join(`${__dirname}/../cheque-verification/main.py`)];
  var formData = new formidable.IncomingForm();

  // Getting the file and fields
  formData.parse(req, (err, fields, files) => {
    // Adding Arguments to pass to python child process
    arr.push(files.myFile.name, fields.account_number);
    // console.log(arr);

    // Running the child process
    const childPython = spawn("python3", arr);

    // Based on the code received after execution return html files
    childPython.on("close", (code) => {
      // console.log(code);
      if (code == 0) {
        res.sendFile(`${__dirname}/public/correct.html`);
      } else {
        res.sendFile(`${__dirname}/public/wrong.html`);
      }
    });
  });
});

app.listen("8000", () => {
  console.log("Server running on port 8000");
});
