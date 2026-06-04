const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());

mongoose.connect("mongodb://127.0.0.1:27017/studentdb")
    .then(() => console.log("MongoDB Connected"))
    .catch(err => console.log(err));

const Student = mongoose.model("Student", {
    name: String,
    marks: Number
});

app.post("/student", async (req, res) => {
    const student = new Student(req.body);
    await student.save();
    res.send("Student Saved");
});

app.get("/students", async (req, res) => {
    const students = await Student.find();
    res.json(students);
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});