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

  let data = [];

  useEffect(() => {
    APICall();
  }, [page]);

  const APICall = () => {
    axios
      .get(
        `https://api.themoviedb.org/3/discover/movie?api_key=8e08b11214706a25758ac317836ef42e&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=${page}&year=2021&with_watch_monetization_types=flatrate`
      )
      .then((res) => {
        let dum_data = res.data["results"];
        console.log(dum_data);
        let dum_arr = [];
        dum_data.map((val, index) => {
          let dum_dic = {};
          let gen_ids = "";
          dum_dic["movie_name"] = val["title"];
          val["genre_ids"].map((val1, ind1) => {
            gen_ids += genres[val1] + ", ";
          });
          dum_dic["genre"] = gen_ids.slice(0, -2);
          dum_dic["year"] = 2021;
          dum_dic["movie_type"] = "Featured Film";
          dum_dic["movie_id"] = val["id"]
          dum_arr.push(dum_dic);
        });
        data = dum_arr;
        console.log(data)
        APItoBackend()
      });
  };

  const APItoBackend = () => {
    const body = {
      data: data,
    };
    console.log("Sending data to backend");
    console.log(data);
    if (data != []) {
      axios
        .post("/api/insert/featuredFilm", body)
        .then((res) => console.log(res));
      if (page <= 499){
        setPage(page+1)
      }
    }
  };

  return (
    <div>
      Hi
      {console.log(data)}
    </div>
  );
};

export default MoviesAPI;
