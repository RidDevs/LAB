const express = require("express");
const userRoutes = require("./144route");

const app = express();

app.use("/users", userRoutes);

app.listen(3000, () => {
    console.log("Server running on port 3000");
});