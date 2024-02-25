const express = require("express");
const spawn = require("child_process").spawn;
const cp = require("child_process");
const router = new express.Router();

router.post("/getphishingurl", async (req, res) => {
  // User will post a list of urls in JSON format
  // { urls: ["abc.xyz","hello.com"]}
  try {
    const url = req.body.url;
    let params = url;
    var command = "python3 -m pipenv run predict ";
    params.forEach((element) => {
      command += element + " ";
    });
    console.log(command);
    cp.exec(command, { cwd: "nlp/" }, (err, stdout, stderr) => {
      console.log(stderr);
      console.log(stdout);
      res.status(200).send({ predicted: stdout });
    });
  } catch (e) {
    console.log(e);
    res.status(400).send({ error: e });
  }
});

module.exports = router;
