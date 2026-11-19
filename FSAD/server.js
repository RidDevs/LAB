const express = require("express");
const app = express();

const logger = (req,res,next)=>{
    console.log(`${req.method} ${req.url}`);
    next();
};

app.use(logger);

app.get("/",(req,res)=>
{res.send("hello express");

});

app.listen(3000,()=>{console.log("running")});