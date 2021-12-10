import { select } from "d3";
import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import axios from "axios";
import ChordChart from "./ChordChart";
import "./ChordChart.css";

const ChordChartValues = () => {
  // main chord values
  //   const [matrix, setMatrix] = useState([]);
  //   const [label_movies_count, setlabel_movies_count] = useState([]);
  //   // 2nd circle => featured + OTT films count
  //   const [film_type_values, setFilmTypeValues] = useState([]);
  //   // 4th circle => genre tweet sentiment
  //   const [tweet_sentiment, setTweetSentmiment] = useState([]);
  const [isDataReceived, setIsDataReceived] = useState(true);

  // dropdown for films
  const [film, setFilm] = useState("Combined Films");
  // dropdown values for filters
  const menu_filters = ["Combined Films", "Feature Films", "OTT Films"];
  // dropdown for states
  const [usStateStr, setusStateStr] = React.useState("California");
  // dropdown values for states
  const states = {
    "All States": "all",
    Alabama: "AL",
    Alaska: "AK",
    Arizona: "AZ",
    Arkansas: "AR",
    California: "CA",
    Colorado: "CO",
    Connecticut: "CT",
    Delaware: "DE",
    "District of Columbia": "AC",
    Florida: "FL",
    Georgia: "GA",
    Hawaii: "HI",
    Idaho: "ID",
    Illinois: "IL",
    Indiana: "IN",
    Iowa: "IA",
    Kansas: "KS",
    Kentucky: "KY",
    Louisiana: "LA",
    Maine: "ME",
    Maryland: "MD",
    Massachusetts: "MA",
    Michigan: "MI",
    Minnesota: "MN",
    Mississippi: "MS",
    Missouri: "MO",
    Montana: "MT",
    Nebraska: "NE",
    Nevada: "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    Ohio: "OH",
    Oklahoma: "OK",
    Oregon: "OR",
    Pennsylvania: "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    Tennessee: "TN",
    Texas: "TX",
    Utah: "UT",
    Vermont: "VT",
    Virginia: "VA",
    Washington: "WA",
    "West Virginia": "WV",
    Wisconsin: "WI",
    Wyoming: "WY",
  };

  // main chord values
  const [matrix, setMatrix] = useState([
    [19, 27, 56, 21, 25, 2, 28, 7, 26, 7],
    [27, 20, 28, 37, 4, 5, 5, 6, 11, 36],
    [56, 28, 4, 17, 7, 1, 17, 2, 17, 17],
    [21, 37, 17, 66, 17, 9, 61, 6, 8, 45],
    [25, 4, 7, 17, 3, 10, 61, 22, 0, 2],
    [2, 5, 1, 9, 10, 225, 4, 1, 1, 4],
    [28, 5, 17, 61, 61, 4, 95, 30, 17, 7],
    [7, 6, 2, 6, 22, 1, 30, 2, 5, 2],
    [26, 11, 17, 8, 0, 1, 17, 5, 10, 5],
    [7, 36, 17, 45, 2, 4, 7, 2, 5, 4],
  ]);
  const [label_movies_count_combined, setlabel_movies_count_combined] =
    useState([141, 111, 86, 255, 130, 301, 375, 79, 79, 78]);
  const [label_movies_count, setlabel_movies_count] = useState([
    [117, 24],
    [76, 35],
    [62, 24],
    [211, 44],
    [100, 30],
    [301, 0],
    [326, 49],
    [68, 11],
    [79, 0],
    [62, 16],
  ]);
  // main chord values
  // ribbon values
  const [ribbon_tweet_count, setribbon_tweet_count] = useState([
    [1420, 19056, 30602, 5684, 13291, 5, 16409, 10970, 13843, 276],
    [19056, 22512, 75758, 75711, 9961, 14056, 5864, 15301, 6002, 75181],
    [30602, 75758, 384, 71704, 703, 4, 12175, 1114, 10466, 67696],
    [5684, 75711, 71704, 5792, 2693, 623, 16075, 1072, 1548, 74204],
    [13291, 9961, 703, 2693, 11, 977, 5943, 12125, 0, 17],
    [5, 14056, 4, 623, 977, 142894, 56, 6, 1, 187],
    [16409, 5864, 12175, 16075, 5943, 56, 39458, 10343, 2823, 9],
    [10970, 15301, 1114, 1072, 12125, 6, 10343, 819, 369, 2],
    [13843, 6002, 10466, 1548, 0, 1, 2823, 369, 3434, 1921],
    [276, 75181, 67696, 74204, 17, 187, 9, 2, 1921, 235],
  ]);
  const [ribbon_avg_senti, setribbon_avg_senti] = useState([
    [0.08, 0.08, 0.1, 0.12, 0.13, 0.05, 0.1, 0.13, 0.06, 0.24],
    [0.08, 0.1, 0.14, 0.16, 0.13, 0.05, 0.11, 0.1, -0.01, 0.16],
    [0.1, 0.14, 0.11, 0.16, 0.13, 0.06, 0.12, 0.13, 0.05, 0.16],
    [0.12, 0.16, 0.16, 0.14, 0.16, 0.06, 0.1, 0.13, 0.18, 0.16],
    [0.13, 0.13, 0.13, 0.16, 0.26, 0.12, 0.12, 0.13, 0, 0.1],
    [0.05, 0.05, 0.06, 0.06, 0.12, 0.11, 0.05, -0.09, 0.0, 0.15],
    [0.1, 0.11, 0.12, 0.1, 0.12, 0.05, 0.15, 0.12, 0.11, 0.22],
    [0.13, 0.1, 0.13, 0.13, 0.13, -0.09, 0.12, 0.09, 0.12, 0.47],
    [0.06, -0.01, 0.05, 0.18, 0, 0.0, 0.11, 0.12, 0.12, 0.15],
    [0.24, 0.16, 0.16, 0.16, 0.1, 0.15, 0.22, 0.47, 0.15, 0.15],
  ]);
  const [ribbon_senti, setribbon_senti] = useState([
    [
      [296, 1008, 116],
      [4766, 12584, 1706],
      [8153, 20196, 2253],
      [1586, 3777, 321],
      [3894, 8529, 868],
      [1, 3, 1],
      [3903, 11352, 1154],
      [3183, 7054, 733],
      [3023, 9468, 1352],
      [133, 136, 7],
    ],
    [
      [4766, 12584, 1706],
      [5637, 15203, 1672],
      [25287, 44618, 5853],
      [26496, 43910, 5305],
      [3008, 6289, 664],
      [2666, 10925, 465],
      [1601, 3794, 469],
      [4225, 9765, 1311],
      [903, 4331, 768],
      [26238, 43691, 5252],
    ],
    [
      [8153, 20196, 2253],
      [25287, 44618, 5853],
      [84, 283, 17],
      [24908, 41698, 5098],
      [200, 463, 40],
      [1, 2, 1],
      [3185, 8330, 660],
      [290, 792, 32],
      [2297, 7137, 1032],
      [23836, 38990, 4870],
    ],
    [
      [1586, 3777, 321],
      [26496, 43910, 5305],
      [24908, 41698, 5098],
      [1822, 3615, 355],
      [923, 1603, 167],
      [132, 427, 64],
      [4017, 10887, 1171],
      [299, 708, 65],
      [569, 890, 89],
      [25906, 43052, 5246],
    ],
    [
      [3894, 8529, 868],
      [3008, 6289, 664],
      [200, 463, 40],
      [923, 1603, 167],
      [7, 3, 1],
      [297, 605, 75],
      [1600, 3952, 391],
      [3537, 7764, 824],
      [0, 0, 0],
      [5, 11, 1],
    ],
    [
      [1, 3, 1],
      [2666, 10925, 465],
      [1, 2, 1],
      [132, 427, 64],
      [297, 605, 75],
      [37858, 96234, 8802],
      [14, 36, 6],
      [0, 4, 2],
      [0, 1, 0],
      [61, 114, 12],
    ],
    [
      [3903, 11352, 1154],
      [1601, 3794, 469],
      [3185, 8330, 660],
      [4017, 10887, 1171],
      [1600, 3952, 391],
      [14, 36, 6],
      [13338, 23487, 2633],
      [2952, 6671, 720],
      [766, 1853, 204],
      [3, 6, 0],
    ],
    [
      [3183, 7054, 733],
      [4225, 9765, 1311],
      [290, 792, 32],
      [299, 708, 65],
      [3537, 7764, 824],
      [0, 4, 2],
      [2952, 6671, 720],
      [181, 582, 56],
      [100, 243, 26],
      [2, 0, 0],
    ],
    [
      [3023, 9468, 1352],
      [903, 4331, 768],
      [2297, 7137, 1032],
      [569, 890, 89],
      [0, 0, 0],
      [0, 1, 0],
      [766, 1853, 204],
      [100, 243, 26],
      [915, 2322, 197],
      [604, 1224, 93],
    ],
    [
      [133, 136, 7],
      [26238, 43691, 5252],
      [23836, 38990, 4870],
      [25906, 43052, 5246],
      [5, 11, 1],
      [61, 114, 12],
      [3, 6, 0],
      [2, 0, 0],
      [604, 1224, 93],
      [79, 146, 10],
    ],
  ]);
  const [ribbon_movies_count, setribbon_movies_count] = useState([
    [19, 27, 56, 21, 25, 2, 28, 7, 26, 7],
    [27, 20, 28, 37, 4, 5, 5, 6, 11, 36],
    [56, 28, 4, 17, 7, 1, 17, 2, 17, 17],
    [21, 37, 17, 66, 17, 9, 61, 6, 8, 45],
    [25, 4, 7, 17, 3, 10, 61, 22, 0, 2],
    [2, 5, 1, 9, 10, 225, 4, 1, 1, 4],
    [28, 5, 17, 61, 61, 4, 95, 30, 17, 7],
    [7, 6, 2, 6, 22, 1, 30, 2, 5, 2],
    [26, 11, 17, 8, 0, 1, 17, 5, 10, 5],
    [7, 36, 17, 45, 2, 4, 7, 2, 5, 4],
  ]);
  // ribbon values
  // tweet values for last circle
  const [tweet_senti_for_last_circle, settweet_senti_for_last_circle] =
    useState([
      [15367, 39352, 4375, 0.1],
      [43367, 91423, 10353, 0.12],
      [33518, 63145, 7366, 0.14],
      [35196, 64068, 7383, 0.15],
      [7089, 15578, 1646, 0.13],
      [54526, 138300, 12014, 0.11],
      [38318, 81045, 8767, 0.13],
      [9893, 24028, 2787, 0.11],
      [6303, 17622, 2223, 0.08],
      [26704, 44735, 5365, 0.16],
    ]);
  const [tweet_count_for_last_circle, settweet_count_for_last_circle] =
    useState([
      59094, 145143, 104029, 106647, 24313, 204840, 128130, 36708, 26148, 76804,
    ]);
  // tweet values for last circle

  const handleFilmChange = (event) => {
    setIsDataReceived(true);
    setFilm(event.target.value);
  };
  const handleStateChange = (event) => {
    setIsDataReceived(true);
    setusStateStr(event.target.value);
  };
  const fetchMatrix = () => {
    let body = {
      movie_type: film,
      state_type: states[usStateStr],
    };
    axios.post("/dropdown-chord-values", body).then((res) => {
      console.log(res["data"]);
      setIsDataReceived(true);
      setlabel_movies_count_combined(
        res["data"]["main_chord_values"]["movies_count_combined"]
      );
      setlabel_movies_count(res["data"]["main_chord_values"]["movies_count"]);
      setribbon_tweet_count(res["data"]["ribbon_values"]["tweet_count"]);
      setribbon_avg_senti(res["data"]["ribbon_values"]["avg_senti"]);
      setribbon_senti(res["data"]["ribbon_values"]["overall_senti"]);
      setribbon_movies_count(res["data"]["ribbon_values"]["movies_count"]);
      settweet_senti_for_last_circle(
        res["data"]["tweet_senti_values"]["tweets_senti_overall"]
      );
      settweet_count_for_last_circle(
        res["data"]["tweet_senti_values"]["tweet_count"]
      );
      setIsDataReceived(false);
      setMatrix(res["data"]["main_chord_values"]["matrix"]);
    });
  };

  useEffect(() => {
    if (isDataReceived) {
      fetchMatrix();
    }
  }, [film, usStateStr, matrix]);
  return (
    <div className="d-flex flex-column justify-content-center main-chord-chart-values">
      <div className="d-flex justify-content-center chord-title">
        Tweet sentiment for different combination of genres based on the film
        types and states
      </div>
      <div className="drop-down d-flex flex-row justify-content-end m-4 p-4">
        <div>
          <InputLabel
            id="demo-simple-select-autowidth-label"
            className="dropdown-label"
          >
            Film Type
          </InputLabel>
          <Select
            sx={{ m: 1, minWidth: 150 }}
            label="Select"
            value={film}
            onChange={handleFilmChange}
            variant="outlined"
          >
            {menu_filters.map((val, index) => (
              <MenuItem value={val} key={index}>
                {val}
              </MenuItem>
            ))}
          </Select>
        </div>
        <div>
          <InputLabel
            id="demo-simple-select-autowidth-label"
            className="dropdown-label"
          >
            States
          </InputLabel>
          <Select
            sx={{ m: 1, minWidth: 150 }}
            label="Select"
            value={usStateStr}
            onChange={handleStateChange}
            variant="outlined"
          >
            {Object.entries(states).map(([key, val]) => (
              <MenuItem value={key} key={val}>
                {key}
              </MenuItem>
            ))}
          </Select>
        </div>
      </div>
      <div className="d-flex justify-content-center chord-chart">
        {!isDataReceived ? (
          <ChordChart
            matrix={matrix}
            label_movies_count_combined={label_movies_count_combined}
            label_movies_count={label_movies_count}
            ribbon_movies_count={ribbon_movies_count}
            ribbon_tweet_count={ribbon_tweet_count}
            ribbon_avg_senti={ribbon_avg_senti}
            ribbon_senti={ribbon_senti}
            tweet_senti_for_last_circle={tweet_senti_for_last_circle}
            tweet_count_for_last_circle={tweet_count_for_last_circle}
            movie_type={film}
          />
        ) : (
          <h1 className="loading-text">Loading....</h1>
        )}
      </div>
    </div>
  );
};

export default ChordChartValues;
