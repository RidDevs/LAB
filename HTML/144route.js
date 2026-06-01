const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.send("All Users");
});

router.get("/:id", (req, res) => {
    res.send(`User ID: ${req.params.id}`);
});

module.exports = router;