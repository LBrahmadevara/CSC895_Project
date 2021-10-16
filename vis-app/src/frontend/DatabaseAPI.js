import React, { useEffect, useState } from "react";
import axios from "axios";

const DatabaseAPI = () => {
  const [mvName, setMvName] = useState("");
  const [mvGenre, setGenre] = useState("");
  const [mvYear, setMvYear] = useState("2021");
  const [updated, setUpdated] = useState(0);
  const [page, setPage] = useState(1);

  useEffect(() => {
    ApiCall();
    // ApiBackend();
  }, [updated]);
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

  //   const dummy = ["12", "14", "36"]
  //   console.log(genres['28'])
  //   let dummy_len = dummy.length -1
  //   let ids = ""
  //   while (dummy_len >= 0) {
  //     ids += genres[dummy[dummy_len]]
  //     dummy_len -= 1
  //     if (dummy_len >= 0){
  //         ids +=", "
  //     }
  //   }
  //   console.log(ids)
  const ApiCall = () => {
    axios
      .get(
        `https://api.themoviedb.org/3/discover/movie?api_key=8e08b11214706a25758ac317836ef42e&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=${page}&year=${mvYear}&with_watch_monetization_types=flatrate`
      )
      .then((res) => {
        // console.log(res.data["results"]);
        let results = res.data["results"];
        for (let i in results) {
          //   console.log(results[i]["original_title"]);
          setMvName(results[i]["original_title"]);
          let ids = "";
          let genre_len = results[i]["genre_ids"].length - 1;
          while (genre_len >= 0) {
            ids += genres[results[i]["genre_ids"][genre_len]];
            genre_len -= 1;
            if (genre_len >= 0) {
              ids += ", ";
            }
          }
          setGenre(ids);
          ApiBackend();
        }
      });
  };
  

  const ApiBackend = () => {
    const body = {
      movie_name: mvName,
      genre: mvGenre,
      year: mvYear,
      movie_type: "Featured Film",
    };
    axios
      .post("/api/data/insert/featuredFilm", body)
      .then((res) => console.log(res));
  };

  return (
    <div>
      Hi
      {/* {console.log(mvGenre)}
      {console.log(mvName)} */}
    </div>
  );
};
export default DatabaseAPI;
