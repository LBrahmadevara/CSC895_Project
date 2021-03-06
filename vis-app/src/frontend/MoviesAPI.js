import React, { useEffect, useState } from "react";
import axios from "axios";

const MoviesAPI = () => {
  const [page, setPage] = useState(1);
  const genres = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
  };

  const OTTgenres = {
    10759: "Action & Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentry",
    18: "Drama",
    10751: "Family",
    10762: "Kids",
    9648: "Mystery",
    10763: "News",
    10764: "Reality",
    10765: "Sci-Fi & Fantasy",
    10766: "Soap",
    10767: "Talk",
    10768: "War & Politics",
    37: "Western",
  };

  let data = [];
  let total_pages = 0;

  useEffect(() => {
    APICall();
    // OTTAPI();
  }, [page]);

  const OTTAPI = () => {
    axios
      .get(
        `https://api.themoviedb.org/3/discover/tv?api_key=8e08b11214706a25758ac317836ef42e&language=en-US&sort_by=popularity.desc&air_date.gte=2021&first_air_date.gte=2021&first_air_date_year=2021&page=${page}&timezone=America%2FNew_York&include_null_first_air_dates=false&with_watch_monetization_types=flatrate`
      )
      .then((res) => {
        console.log("Original", res["data"]);
        total_pages = res["data"]["total_pages"];
        let results = res["data"]["results"];
        let dum_arr = [];
        results.map((val, index) => {
          if ((val["genre_ids"].length !== 0) && (val["original_language"] === "en")) {
            let dum_dic = {};
            let gen_ids = "";
            dum_dic["movie_name"] = val["name"];
            val["genre_ids"].map((val1, ind1) => {
              gen_ids += OTTgenres[val1] + ", ";
            });
            dum_dic["genre"] = gen_ids.slice(0, -2);
            dum_dic["year"] = 2021;
            dum_dic["movie_type"] = "OTT Film";
            dum_dic["movie_id"] = val["id"];
            dum_dic["release_date"] = val["first_air_date"];
            dum_arr.push(dum_dic);
          }
        });
        data = dum_arr;
        console.log("Structured: ", data);
        OTTtoBackend();
      });
  };


  const APICall = () => {
    axios
      .get(
        `https://api.themoviedb.org/3/discover/movie?api_key=8e08b11214706a25758ac317836ef42e&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=${page}&primary_release_year=2021&primary_release_date.gte=2021&release_date.gte=2021&year=2021&with_watch_monetization_types=flatrate`
      )
      .then((res) => {
        let dum_data = res.data["results"];
        total_pages = res["data"]["total_pages"];
        console.log(dum_data);
        let dum_arr = [];
        dum_data.map((val, index) => {
          if ((val["genre_ids"].length !== 0) && (val["original_language"] === "en")) {
            let dum_dic = {};
            let gen_ids = "";
            // movie_name => this gives the name of the movie
            dum_dic["movie_name"] = val["title"];
            // genre_ids => gives the list of id's
            val["genre_ids"].map((val1, ind1) => {
              gen_ids += genres[val1] + ", ";
            });
            // map the list of ids to names and retrieving genre names
            dum_dic["genre"] = gen_ids.slice(0, -2);
            // add specific movie_type to distingush between feature and over-the-top media service
            dum_dic["movie_type"] = "Featured Film";
            // movie_id => this is just for the future reference, this is a unique id for a movie in the API
            dum_dic["movie_id"] = val["id"];
            // release_date => shows the exact date when the movie was released
            dum_dic["release_date"] = val["release_date"];
            dum_dic["year"] = 2021;
            dum_arr.push(dum_dic);
          }
        });
        data = dum_arr;
        console.log(data);
        APItoBackend();
      });
  };

  const OTTtoBackend = () => {
    let last_page = false
    if (page === total_pages){
      last_page = true
      console.log("Last_page")
    }
    const body = {
      data: data,
      last_page: last_page
    };
    if (data !== []) {
      axios.post("/OTTmovies", body).then((res) => {
        console.log("res", res);
      });
      if (page <= total_pages) {
        setPage(page + 1);
      }
    }
  };

  const APItoBackend = () => {
    // console.log("Sending data to backend");
    if (data !== []) {
      const body = {
        data: data,
      };
      // axios.post("/api/insert/featuredFilm", body)
      axios.post("/movieTable", body).then((res) => {
        console.log("res", res);
      });
      console.log("total Pages: ", total_pages);
      if (page <= total_pages) {
        setPage(page + 1);
      }
    }
  };

  return <div>{console.log(data)}</div>;
};

export default MoviesAPI;
