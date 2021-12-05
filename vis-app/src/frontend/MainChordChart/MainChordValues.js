import { select } from "d3";
import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import axios from "axios";
import ChordTest1 from "./ChordTest1";
import "./Chord.css";

const MainChordValues = () => {
  // main chord values
  const [matrix, setMatrix] = useState([]);
  const [combined_movies_count, setcombined_movies_count] = useState([]);
  // 2nd circle => featured + OTT films count
  const [film_type_values, setFilmTypeValues] = useState([]);
  // 4th circle => genre tweet sentiment
  const [tweet_sentiment, setTweetSentmiment] = useState([]);
  const [isDataReceived, setIsDataReceived] = useState(false);

  // dropdown for films
  const [film, setFilm] = useState("Combined Films");
  // dropdown values for filters
  const menu_filters = ["Combined Films", "Feature Films", "OTT Films"];
  // dropdown for states
  const [usStateStr, setusStateStr] = React.useState("California");
  // dropdown values for states
  const states = [
    "All States",
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "District of Columbia",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
  ];

  // combined tweet sentiment => for ribbon label
  const [combined_genres_tweets_senti, setcombined_genres_tweets_senti] =
    useState([]);
  // combined genre tweets count => for ribbon label (
  // contains total tweet, +ve, -ve, neutral count and avg sentiment)
  const [combined_genres_tweets, setcombined_genres_tweets] = useState([]);

  // overall sentiment for a genre => for last circle label
  const [overall_senti, setoverall_senti] = useState([]);
  // tweet count for genre => for last circle label
  const [tweet_count_per_genre, settweet_count_per_genre] = useState([]);

  const fetchMatrix = () => {
    if (film === "Combined Films") {
      axios.get("/chord-ribbon-values").then((res) => {
        setIsDataReceived(false);
        setMatrix(res["data"]["chord_values"]);
        setcombined_movies_count(res["data"]["combined_movies_count"])
        setFilmTypeValues(res["data"]["film_type"]);
        setTweetSentmiment(res["data"]["tweet_sentiment_combined"]);
        console.log(res["data"]["tweet_sentiment_combined"]);
        setcombined_genres_tweets_senti(
          res["data"]["combined_genres_tweets"]["senti"]
        );
        setcombined_genres_tweets(
          res["data"]["combined_genres_tweets"]["chord_values"]
        );
        setoverall_senti(res["data"]["combined_overall_sentiment"]);
        settweet_count_per_genre(res["data"]["combined_TweetCountPerGenre"]);
        setIsDataReceived(true);
      });
    } else if (film === "Feature Films") {
      // axios.get("/chord-ribbon-values-movie-type").then((res) => {
      //   setIsDataReceived(false);
      //   setMatrix(res["data"]["feature_data"]);
      //   setTweetSentmiment(res["data"]["tweet_sentiment_featured"]);
      //   setcombined_genres_tweets_senti(
      //     res["data"]["combined_genres_tweets"]["senti"]
      //   );
      //   setcombined_genres_tweets(
      //     res["data"]["combined_genres_tweets"]["chord_values"]
      //   );
      //   setoverall_senti(res["data"]["overall_sentiment"]);
      //   settweet_count_per_genre(res["data"]["TweetCountPerGenre"]);
      //   setIsDataReceived(true);
      // });
      axios.get("/chord-ribbon-values").then((res) => {
        setIsDataReceived(false);
        setMatrix(res["data"]["feature_chord_values"]);
        console.log(res["data"]["feature_chord_values"])
        setTweetSentmiment(res["data"]["tweet_sentiment_featured"]);
        setcombined_genres_tweets_senti(
          res["data"]["featured_genres_tweets"]["senti"]
        );
        setcombined_genres_tweets(
          res["data"]["featured_genres_tweets"]["chord_values"]
        );
        setoverall_senti(res["data"]["featured_overall_sentiment"]);
        settweet_count_per_genre(res["data"]["feature_TweetCountPerGenre"]);
        setIsDataReceived(true);
      });
    } else if (film === "OTT Films") {
      axios.get("/chord-ribbon-values").then((res) => {
        setIsDataReceived(false);
        setMatrix(res["data"]["ott_chord_values"]);
        setTweetSentmiment(res["data"]["tweet_sentiment_OTT"]);
        setcombined_genres_tweets_senti(
          res["data"]["OTT_genres_tweets"]["senti"]
        );
        setcombined_genres_tweets(
          res["data"]["OTT_genres_tweets"]["chord_values"]
        );
        setoverall_senti(res["data"]["ott_overall_sentiment"]);
        settweet_count_per_genre(res["data"]["ott_TweetCountPerGenre"]);
        setIsDataReceived(true);
      });
    }
  };
  const handleFilmChange = (event) => {
    setFilm(event.target.value);
  };
  const handleStateChange = (event) => {
    setusStateStr(event.target.value);
  };

  useEffect(() => {
    fetchMatrix();
  }, [film]);
  return (
    <div className="d-flex flex-column justify-content-center">
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
            // val="asd"
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
            {states.map((val, index) => (
              <MenuItem value={val} key={index}>
                {val}
              </MenuItem>
            ))}
          </Select>
        </div>
      </div>
      <div className="d-flex justify-content-center chord-chart">
        {isDataReceived && (
          <ChordTest1
            matrix={matrix}
            film={film}
            usStateStr={usStateStr}
            film_type_values={film_type_values}
            tweet_senti={tweet_sentiment}
            combined_genres_tweets_senti={combined_genres_tweets_senti}
            combined_genres_tweets={combined_genres_tweets}
            overall_senti={overall_senti}
            tweet_count={tweet_count_per_genre}
            combined_movies_count = {combined_movies_count}
          />
        )}
        {isDataReceived && console.log(film_type_values)}
      </div>
    </div>
  );
};

export default MainChordValues;
