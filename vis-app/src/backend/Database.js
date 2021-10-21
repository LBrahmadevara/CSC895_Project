const express = require("express");
var mysql = require("mysql");
const app = express();
const axios = require("axios");
const port = 5000;

app.use(express.json());

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Login@123",
  database: "Master_Final",
});

con.connect(function (err) {
  if (err) throw err;

  app.post("/api/insert/featuredFilm", (req, res) => {
    const {data} = req.body;
    let sqlQuery = "INSERT INTO Master_Final.movies1 (";
    let queryextn = "";
    let queryextnVal = "";
    data.map((val, index) => {
      Object.entries(val).map(([key, value]) => {
        queryextn += key + ", ";
        queryextnVal += "'" + value + "', ";
      });
      queryextn = queryextn.slice(0, -2) + ") VALUES (";
      queryextnVal = queryextnVal.slice(0, -2) + ");";
      con.query(sqlQuery+queryextn+queryextnVal, function(err, result){
        if (err) {
          console.log("error: ", err);
        } else {
          console.log(result)
        }
      })
      queryextn = "";
      queryextnVal = "";
    });
    res.send({ isDataSent: true });
  })

  app.post("/api/insert/OTTFilm", (req, res) => {
    const {data} = req.body;
    let sqlQuery = "INSERT INTO Master_Final.movies1 (";
    let queryextn = "";
    let queryextnVal = "";
    data.map((val, index) => {
      Object.entries(val).map(([key, value]) => {
        queryextn += key + ", ";
        queryextnVal += "'" + value + "', ";
      });
      queryextn = queryextn.slice(0, -2) + ") VALUES (";
      queryextnVal = queryextnVal.slice(0, -2) + ");";
      con.query(sqlQuery+queryextn+queryextnVal, function(err, result){
        if (err) {
          console.log("error: ", err);
        } else {
          console.log(result)
        }
      })
      queryextn = "";
      queryextnVal = "";
    });
    res.send({ isDataSent: true });
  })

  app.listen(port, () => console.log(`Example app listening on port ${port}!`));
});
