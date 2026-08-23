const express = require("express");
const app = express();

const userRoutes = require("./144route");

app.use("/user", userRoutes);

app.listen(3000, () => {
    console.log("Server running on port 3000");
});