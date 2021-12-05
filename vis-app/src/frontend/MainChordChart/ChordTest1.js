import { select } from "d3";
import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import axios from "axios";

const ChordTest1 = (props) => {
  let matrix = props.matrix;
  const svgRef = useRef();
  const genres = [
    "Action",
    "Animation",
    "Adventure",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Mystery",
    "Science Fiction",
    "Family",
  ];
  const colors = [
    "#c4c4c4",
    "rgb(154 203 94)",
    "rgb(217 90 95)",
    "rgb(171 132 213)",
    "rgb(168 171 121)",
    "rgb(67 76 133)",
    "rgb(77 120 90)",
    "#737373",
    "#c3c370",
    "#f3ae5d",
  ];
  const combined_movies_count = props.combined_movies_count;
  const film_colors = ["#bb6e4e", "black"];
  const senti_colors = ["green", "#36369f", "red"];
  const tweet_senti = props.tweet_senti;
  // console.log(tweet_senti)
  const overall_senti = props.overall_senti;
  const tweet_count = props.tweet_count;
  const combined_genres_tweets = props.combined_genres_tweets;
  const combined_genres_tweets_senti = props.combined_genres_tweets_senti;
  const film_types = props.film_type_values;
  let tweet_senti_states = [
    [8270, 19704, 14454],
    [2262, 7179, 5819],
    [17533, 43504, 32612],
    [3812, 9560, 7164],
    [129768, 310644, 228437],
    [14142, 35658, 26561],
    [7824, 18105, 13221],
    [877, 2657, 1821],
    [8019, 21820, 15698],
    [57208, 143331, 109475],
    [21235, 56953, 43115],
    [4359, 10432, 7880],
    [2282, 5479, 4064],
    [32466, 78167, 57069],
    [14517, 34382, 25223],
    [5507, 12356, 9048],
    [5075, 11325, 8115],
    [7183, 16678, 12113],
    [10752, 29836, 22618],
    [1864, 4306, 3064],
    [16103, 41565, 31119],
    [20029, 46833, 33708],
    [16621, 40460, 29852],
    [10635, 24493, 17450],
    [3175, 7581, 5677],
    [11863, 28311, 20701],
    [1018, 2499, 1720],
    [4076, 9350, 6562],
    [13083, 30645, 22685],
    [2003, 4905, 3574],
    [20883, 53854, 39994],
    [3312, 8840, 6228],
    [68887, 178947, 126031],
    [30479, 85970, 68401],
    [1478, 2773, 1908],
    [26180, 61197, 44690],
    [11771, 27446, 20573],
    [10683, 27484, 20667],
    [24200, 60809, 44922],
    [2926, 6853, 5055],
    [7513, 19251, 14613],
    [996, 2528, 1839],
    [16298, 37957, 27687],
    [94997, 220404, 164576],
    [6599, 15530, 11174],
    [690, 1728, 1259],
    [18061, 43901, 32207],
    [19334, 46772, 33552],
    [2277, 5073, 3561],
    [7525, 17743, 12939],
    [562, 1295, 963],
  ];

  let movies_count_states = [
    619, 372, 782, 508, 1301, 724, 622, 343, 645, 999, 790, 518, 438, 894, 720,
    544, 544, 626, 648, 408, 761, 817, 764, 676, 457, 708, 326, 508, 753, 427,
    815, 502, 1134, 774, 378, 814, 622, 674, 824, 478, 609, 320, 724, 1085, 621,
    311, 794, 789, 420, 633, 264,
  ];
  let featured_matrix = [
    [23, 17, 34, 19, 29, 2, 25, 8, 26, 5],
    [17, 22, 19, 28, 3, 6, 4, 5, 12, 33],
    [34, 19, 4, 13, 6, 2, 11, 2, 17, 15],
    [19, 28, 13, 67, 21, 9, 82, 6, 11, 44],
    [29, 3, 6, 21, 3, 12, 64, 25, 0, 1],
    [2, 6, 2, 9, 12, 313, 5, 1, 2, 4],
    [25, 4, 11, 82, 64, 5, 124, 30, 18, 12],
    [8, 5, 2, 6, 25, 1, 30, 2, 6, 2],
    [26, 12, 17, 11, 0, 2, 18, 6, 15, 5],
    [5, 33, 15, 44, 1, 4, 12, 2, 5, 4],
  ];
  let OTT_matrix = [
    [23, 14, 27, 6, 2, 0, 8, 0, 16, 3],
    [14, 22, 14, 17, 1, 0, 4, 1, 16, 10],
    [27, 14, 4, 6, 2, 0, 8, 0, 16, 3],
    [6, 17, 6, 67, 3, 0, 9, 1, 3, 12],
    [2, 1, 2, 3, 3, 0, 14, 6, 3, 1],
    [0, 0, 0, 0, 0, 313, 0, 0, 0, 0],
    [8, 4, 8, 9, 14, 0, 124, 8, 15, 0],
    [0, 1, 0, 1, 6, 0, 8, 2, 4, 0],
    [16, 16, 16, 3, 3, 0, 15, 4, 15, 1],
    [3, 10, 3, 12, 1, 0, 0, 0, 1, 4],
  ];

  //Initialize canvas and inner/outer radii of the chords
  const width = 1200,
    height = 1200,
    outerRadius = 550,
    innerRadius = outerRadius - 20;
  // for dropdowns
  const film = props.film;
  const usStateStr = props.usStateStr;

  // for dropdowns

  const tweet_sentiment_angles = (angles_arr, backend_senti_arr, film) => {
    let data_groups = [];
    angles_arr.map((item, index) => {
      let difference = item["endAngle"] - item["startAngle"];
      let e1 = {};
      e1["index"] = item["index"];
      e1["color"] = 0;
      e1["startAngle"] = item["startAngle"];
      e1["endAngle"] =
        e1["startAngle"] +
        difference *
          (backend_senti_arr[index][0] / d3.sum(backend_senti_arr[index]));
      data_groups.push(e1);
      let e2 = {};
      if (!film) {
        e2["index"] = item["index"];
        e2["color"] = 1;
        e2["startAngle"] = e1["endAngle"];
        e2["endAngle"] =
          e2["startAngle"] +
          difference *
            (backend_senti_arr[index][1] / d3.sum(backend_senti_arr[index]));
        data_groups.push(e2);
      }
      let e3 = {};
      e3["index"] = item["index"];
      if (!film) {
        e3["color"] = 2;
        e3["startAngle"] = e2["endAngle"];
      } else {
        e3["color"] = 1;
        e3["startAngle"] = e1["endAngle"];
      }

      e3["endAngle"] = item["endAngle"];
      data_groups.push(e3);
    });
    return data_groups;
  };
  const pie_data_padangle = (p_data) => {
    const pie = d3.pie();
    const pie_data = pie(p_data);
    let pie_data_with_padangle = [];
    pie_data.map((item, ind) => {
      let y = {};
      y["data"] = item["data"];
      y["value"] = item["value"];
      y["endAngle"] = Number(item["endAngle"] - 0.011);
      y["startAngle"] = item["startAngle"];
      y["padAngle"] = 0;
      y["index"] = ind
      y["value"] = item["value"];
      pie_data_with_padangle.push(y);
    });
    return pie_data_with_padangle;
  };
  useEffect(async () => {
    // await axios.get("/chord-sentiment").then((res) => {
    //   senti = res["data"]["data"];
    // });
    // await axios.get("/chord-ribbon-values").then((res) => {
    //   matrix = res["data"]["chord_values"];
    // });
    // await axios.get("/overall-senti").then((res) => {
    //   // console.log(res)
    //   overall_senti = res["data"]["data"];
    // });
    // await axios.get("/tweet-count").then((res) => {
    //   tweet_count = res["data"]["data"];
    // });
    // await axios.get("/tweets-for-combined-genres").then((res) => {
    //     combined_genres_tweets = res["data"]["chord_values"]
    //     combined_genres_tweets_senti = res["data"]["senti"]
    // })

    // const svg = select(svgRef.current);

    // if (matrix !== []) {
    const totalDataSum = d3.sum(matrix.flat());
    const fade = (opacity) => {
      return (d, i) => {
        ribbons
          .filter(
            (d) => d.source.index !== i.index && d.target.index !== i.index
          )
          .transition()
          .style("opacity", opacity);
        group3
          .filter((d) => d.index !== i.index)
          .transition()
          .style("opacity", opacity);
        group2
          .filter((d) => d.index !== i.index)
          .transition()
          .style("opacity", opacity);
        if (film === "Combined Films") {
          film_group
            .filter((d) => d.index !== i.index)
            .transition()
            .style("opacity", opacity);
        }
      };
    };

    const chord = d3
      .chord()
      .padAngle(0.01)
      .sortSubgroups(d3.descending)
      .sortChords(d3.descending);
    //Set Arc Raddii
    const arc = d3.arc();

    //Set Ribbbons
    const ribbon = d3
      .ribbon()
      .radius(innerRadius - 12)
      .padAngle(3 / innerRadius);

    //Initialize colors to an ordinal scheme with 10 categories
    const color = d3.scaleOrdinal(genres, colors);
    console.log(matrix)
    let chord_data = chord(matrix);

    const svg = d3.selectAll("svg");
    svg.selectAll("*").remove();
    const g = svg
      .append("g")
      //   .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
      .attr("transform", "translate(650,700)")
      .datum(chord_data);

    //Defines each "group" in the chord diagram
    const group = g
      .append("g")
      .attr("class", "groups")
      .selectAll("g")
      .data(chord_data.groups)
      .enter()
      .append("g");
    g.select("groups").remove();

    //Draw the radial arcs for each group
    group
      .append("path")
      .attr("id", (d) => {
        return "movies_" + d.index;
      })
      .style("fill", function (d) {
        return color(genres[d.index]);
      })
      .attr("d", arc.innerRadius(innerRadius).outerRadius(outerRadius))
      .on("mouseover", fade(0.1))
      .on("mouseout", fade(1));

    group
      .append("title")
      .text(
        (d) =>
          `Genre: ${genres[d.index]} \nTotal Number of Movies: ${
            // film_types[d.index][2]
            // d.value
            combined_movies_count[d.index]
          } movies(${((d.value / totalDataSum) * 100).toFixed(
            2
          )}%) \nNumber of Feature Films: ${
            film_types[d.index][0]
          } \nNumber of OTT Films: ${film_types[d.index][1]}`
      );
    if (film !== "Combined Films") {
      group
        .selectAll(".names")
        .data(genres)
        .enter()
        .append("text")
        .attr("class", "names")
        .append("textPath")
        .attr("xlink:href", function (d, i) {
          return "#movies_" + i;
        })
        .text((d) => d)
        .style("font-size", "20px")
        .style("font-weight", "normal");
    }

    // film type
    let film_chord = tweet_sentiment_angles(
      chord_data.groups,
      film_types,
      true
    );
    // console.log(film_types)
    const film_group = g
      .append("g")
      .attr("class", "film_group")
      .selectAll("g")
      .data(film_chord)
      .enter()
      .append("g");
    if (film === "Combined Films") {
      film_group
        .append("path")
        .attr("id", (d) => {
          return "genre_" + d.index;
        })
        .style("fill", function (d) {
          return film_colors[d["color"]];
        })
        .attr(
          "d",
          arc
            .innerRadius(innerRadius + 20)
            .outerRadius(outerRadius + 8)
            .startAngle((d) => d["startAngle"])
            .endAngle((d) => d["endAngle"])
        );
      film_group
        .selectAll(".names")
        .data(genres)
        .enter()
        .append("text")
        .attr("class", "names")
        .append("textPath")
        .attr("xlink:href", function (d, i) {
          return "#genre_" + i;
        })
        .text((d) => d)
        .style("font-size", "22px")
        .style("font-weight", "normal");
    }
    // film type

    // // Logic for TweetCount
    let tweet_data = pie_data_padangle(tweet_count);
    const group2 = g
      .append("g")
      .attr("class", "groups2")
      .selectAll("g")
      .data(tweet_data)
      .enter()
      .append("g");
    group2
      .append("path")
      .style("fill", function (d) {
        return colors[d["index"]];
      })
      .attr(
        "d",
        arc
          .innerRadius(innerRadius + 56)
          .outerRadius(outerRadius + 44)
          .startAngle((d) => d["startAngle"])
          .endAngle((d) => d["endAngle"])
      );
      //to display text just for reference
      // group2.append("text")
			// .attr("transform",(d)=>{
			// 		return "translate("+
			// 		arc.centroid(d) + ")";
			// })
			// .text(function(d){
			// return d.data;
			// });
//to display text just for reference
    // Logic for TweetCount

    // Logic for Tweet Count Sentiment
    let tweet_count_senti_groups = tweet_sentiment_angles(
      tweet_data,
      tweet_senti,
      false
    );
    // console.log(tweet_data);
    // console.log(d3.sum(tweet_count));
    // console.log(tweet_senti);
    console.log(tweet_count_senti_groups);
    // tweet_count_senti_groups = []
    const group3 = g
      .append("g")
      .attr("class", "groups3")
      .selectAll("g")
      .data(tweet_count_senti_groups)
      .enter()
      .append("g");
    group3
      .append("path")
      .style("fill", function (d) {
        return senti_colors[d["color"]];
      })
      .attr(
        "d",
        arc
          .innerRadius(innerRadius + 64)
          .outerRadius(outerRadius + 69)
          .startAngle((d) => d["startAngle"])
          .endAngle((d) => d["endAngle"])
      )
      .on("mouseover", fade(0.1))
      .on("mouseout", fade(1))
      .append("title")
      .text((d) => {
        return `Genre: ${genres[d["index"]]} \nTotal Tweets: ${
        //   tweet_senti[d["index"]][0]+tweet_senti[d["index"]][1]+tweet_senti[d["index"]][2]
        // } (${((tweet_count[d["index"]] / d3.sum(tweet_count)) * 100).toFixed(
        //   2
          tweet_count[d["index"]]
        } (${((tweet_count[d["index"]] / d3.sum(tweet_count)) * 100).toFixed(
          2
        )}%) \nNumber of +ve Tweets: ${
          tweet_senti[d["index"]][0]
        } \nNumber of Neutral Tweets: ${
          tweet_senti[d["index"]][2]
        }  \nNumber of -ve Tweets: ${
          tweet_senti[d["index"]][1]
        } \nAverage Tweets Sentiment: ${overall_senti[d["index"]]}`;
      });
    // Logic for Tweet Count Sentiment

    const ribbonFade = (opacity) => {
      return (d, i) => {
        ribbons
          .filter((d) => {
            return !(
              d.source.index === i.source.index &&
              d.target.index === i.target.index
            );
          })
          .transition()
          .style("opacity", opacity);
        group3
          .filter((d) => {
            return !(d.index === i.source.index || d.index === i.target.index);
          })
          .transition()
          .style("opacity", opacity);
        group2
          .filter((d) => {
            return !(d.index === i.source.index || d.index === i.target.index);
          })
          .transition()
          .style("opacity", opacity);
        group
          .filter((d) => {
            return !(d.index === i.source.index || d.index === i.target.index);
          })
          .transition()
          .style("opacity", opacity);
        if (film === "Combined Films") {
          film_group
            .filter((d) => {
              return !(
                d.index === i.source.index || d.index === i.target.index
              );
            })
            .transition()
            .style("opacity", opacity);
        }
      };
    };

    //Draw the ribbons that go from group to group
    const ribbons = g
      .append("g")
      .attr("class", "ribbons")
      .selectAll("path")
      .data(function (chords) {
        return chords;
      })
      .enter()
      .append("path")
      .style("fill", (d) => {
        return color(genres[d.target.index]);
      })
      .attr("d", ribbon)
      .on("mouseover", ribbonFade(0.1))
      .on("mouseout", ribbonFade(1));

    ribbons.append("title").text((d) => {
      return d.source.index === d.target.index
        ? `${genres[d.source.index]} have ${d.source.value} movies \nand ${
            combined_genres_tweets[d.source.index][d.target.index]
          } Tweets \nNumber of +ve Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][0]
          }  \nNumber of Nuetral Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][1]
          } \nNumber of -ve Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][2]
          } \nAverage Tweets Sentiment: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][3]
          }`
        : `${genres[d.target.index]} and ${genres[d.source.index]} have \n${
            d.source.value + d.target.value
          } movies and ${
            combined_genres_tweets[d.source.index][d.target.index]
          } Tweets\nNumber of +ve Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][0]
          } \nNumber of Nuetral Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][1]
          } \nNumber of -ve Tweets: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][2]
          } \nAverage Tweets Sentiment: ${
            combined_genres_tweets_senti[d.source.index][d.target.index][3]
          }`;
    });
    // }
  }, [film, usStateStr]);
  return (
    // <div className="d-flex flex-column justify-content-center">
    //   <div className="d-flex flex-row justify-content-end m-4 p-4">
    //     <div>
    //       <InputLabel
    //         id="demo-simple-select-autowidth-label"
    //         className="dropdown-label"
    //       >
    //         Film Type
    //       </InputLabel>
    //       <Select
    //         sx={{ m: 1, minWidth: 150 }}
    //         label="Select"
    //         value={film}
    //         // val="asd"
    //         onChange={handleFilmChange}
    //         variant="outlined"
    //       >
    //         {menu_filters.map((val, index) => (
    //           <MenuItem value={val} key={index}>
    //             {val}
    //           </MenuItem>
    //         ))}
    //       </Select>
    //     </div>
    //     <div>
    //       <InputLabel
    //         id="demo-simple-select-autowidth-label"
    //         className="dropdown-label"
    //       >
    //         States
    //       </InputLabel>
    //       <Select
    //         sx={{ m: 1, minWidth: 150 }}
    //         label="Select"
    //         value={usStateStr}
    //         onChange={handleStateChange}
    //         variant="outlined"
    //       >
    //         {states.map((val, index) => (
    //           <MenuItem value={val} key={index}>
    //             {val}
    //           </MenuItem>
    //         ))}
    //       </Select>
    //     </div>
    //   </div>
    //   <div className="d-flex justify-content-center chord-chart">
    //     <svg width="1300" height="1800">
    //       {/* <g className="groups" /> */}
    //     </svg>
    //   </div>
    // </div>

    <svg ref={svgRef} width="1300" height="1800"></svg>
  );
};
export default ChordTest1;
