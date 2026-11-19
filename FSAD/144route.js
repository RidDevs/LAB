const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.send("All Users");
});

router.get("/1", (req, res) => {
    res.send(`User ID: 1`);
});

module.exports = router;