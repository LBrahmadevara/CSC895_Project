import { select } from "d3";
import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import axios from "axios";

const ChordChart = (props) => {
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
  const film_colors = ["#bb6e4e", "black"];
  const senti_colors = ["green", "#36369f", "red"];
  //   let senti = [];
  //   let matrix = [];
  //   let overall_senti = [];
  //   let tweet_count = [];
  //   let combined_genres_tweets = [];
  //   let combined_genres_tweets_senti = [];
  //   let film_types = [];
  let tweet_senti = [
    [75144, 221043, 165311],
    [226609, 528961, 401048],
    [180889, 370916, 273939],
    [178960, 355161, 257123],
    [36012, 90275, 69211],
    [295163, 768293, 566943],
    [230810, 537812, 400424],
    [47366, 121737, 95036],
    [32688, 106334, 80310],
    [132832, 240994, 174601],
  ];
  let matrix = [
    [23, 31, 61, 25, 31, 2, 33, 8, 42, 8],
    [31, 25, 33, 45, 4, 6, 8, 6, 28, 43],
    [61, 33, 4, 19, 8, 2, 19, 2, 33, 18],
    [25, 45, 19, 86, 24, 9, 91, 7, 14, 56],
    [31, 4, 8, 24, 6, 12, 78, 31, 3, 2],
    [2, 6, 2, 9, 12, 313, 5, 1, 2, 4],
    [33, 8, 19, 91, 78, 5, 141, 38, 33, 12],
    [8, 6, 2, 7, 31, 1, 38, 3, 10, 2],
    [42, 28, 33, 14, 3, 2, 33, 10, 15, 6],
    [8, 43, 18, 56, 2, 4, 12, 2, 6, 7],
  ];
  let senti = [
    [40, 127, 15],
    [43, 92, 9],
    [28, 68, 5],
    [155, 197, 31],
    [48, 122, 26],
    [100, 302, 60],
    [188, 320, 60],
    [31, 69, 10],
    [21, 73, 13],
    [43, 55, 7],
  ];
  let overall_senti = [
    0.19, 0.23, 0.22, 0.24, 0.18, 0.17, 0.22, 0.21, 0.18, 0.24,
  ];
  let tweet_count = [
    303873, 778498, 567221, 551162, 129781, 1088056, 788411, 175213, 142878,
    386474,
  ];
  let combined_genres_tweets = [
    [7859, 91735, 150667, 27845, 64036, 45, 84848, 51188, 131432, 1098],
    [91735, 171273, 374162, 380626, 47526, 60135, 30258, 75766, 62511, 376769],
    [150667, 374162, 1568, 355148, 3430, 38, 113250, 2665, 109387, 334269],
    [27845, 380626, 355148, 30237, 12593, 3711, 90621, 6291, 6892, 373802],
    [64036, 47526, 3430, 12593, 46, 5284, 40205, 59177, 352, 76],
    [45, 60135, 38, 3711, 5284, 751871, 211, 300, 15, 1619],
    [84848, 30258, 113250, 90621, 40205, 211, 228378, 47325, 90045, 99],
    [51188, 75766, 2665, 6291, 59177, 300, 47325, 4703, 35304, 4],
    [131432, 62511, 109387, 6892, 352, 15, 90045, 35304, 17292, 9370],
    [1098, 376769, 334269, 373802, 76, 1619, 99, 4, 9370, 1138],
  ];
  let combined_genres_tweets_senti = [
    [
      [1607, 5938, 4719, 0.06],
      [21176, 68109, 51558, 0.07],
      [38870, 108537, 81363, 0.1],
      [7909, 19400, 13701, 0.13],
      [17833, 44546, 33265, 0.12],
      [10, 34, 26, 0.06],
      [20456, 62224, 44453, 0.1],
      [14267, 35434, 26919, 0.12],
      [30541, 97740, 74172, 0.08],
      [524, 560, 400, 0.25],
    ],
    [
      [21176, 68109, 51558, 0.07],
      [40919, 126569, 101027, 0.1],
      [123712, 238240, 172189, 0.14],
      [131639, 236354, 171393, 0.16],
      [13398, 32815, 25023, 0.12],
      [12727, 46363, 36484, 0.06],
      [8513, 20772, 14821, 0.11],
      [19660, 53028, 42320, 0.1],
      [13764, 47138, 35906, 0.06],
      [129940, 234451, 169684, 0.16],
    ],
    [
      [38870, 108537, 81363, 0.1],
      [123712, 238240, 172189, 0.14],
      [461, 1073, 810, 0.14],
      [123125, 220468, 157949, 0.16],
      [1000, 2355, 1760, 0.14],
      [8, 30, 21, 0.08],
      [33007, 78559, 60680, 0.12],
      [784, 1846, 1431, 0.15],
      [26725, 80185, 60646, 0.09],
      [117237, 205811, 147670, 0.16],
    ],
    [
      [7909, 19400, 13701, 0.13],
      [131639, 236354, 171393, 0.16],
      [123125, 220468, 157949, 0.16],
      [9162, 20332, 15318, 0.14],
      [4261, 7972, 6077, 0.16],
      [725, 2797, 2308, 0.04],
      [22750, 65537, 45144, 0.1],
      [1821, 4334, 3113, 0.14],
      [2561, 4150, 3095, 0.18],
      [129216, 232209, 167864, 0.16],
    ],
    [
      [17833, 44546, 33265, 0.12],
      [13398, 32815, 25023, 0.12],
      [1000, 2355, 1760, 0.14],
      [4261, 7972, 6077, 0.16],
      [21, 25, 16, 0.23],
      [1498, 3648, 2647, 0.12],
      [10497, 28764, 22593, 0.12],
      [16527, 40987, 31235, 0.12],
      [111, 234, 176, 0.16],
      [20, 54, 37, 0.1],
    ],
    [
      [10, 34, 26, 0.06],
      [12727, 46363, 36484, 0.06],
      [8, 30, 21, 0.08],
      [725, 2797, 2308, 0.04],
      [1498, 3648, 2647, 0.12],
      [203287, 530585, 394889, 0.12],
      [45, 154, 132, 0.04],
      [88, 207, 169, 0.14],
      [2, 12, 9, 0.05],
      [511, 1082, 875, 0.16],
    ],
    [
      [20456, 62224, 44453, 0.1],
      [8513, 20772, 14821, 0.11],
      [33007, 78559, 60680, 0.12],
      [22750, 65537, 45144, 0.1],
      [10497, 28764, 22593, 0.12],
      [45, 154, 132, 0.04],
      [70420, 152110, 111612, 0.14],
      [13968, 31891, 24957, 0.13],
      [25110, 61972, 48377, 0.12],
      [31, 67, 39, 0.16],
    ],
    [
      [14267, 35434, 26919, 0.12],
      [19660, 53028, 42320, 0.1],
      [784, 1846, 1431, 0.15],
      [1821, 4334, 3113, 0.14],
      [16527, 40987, 31235, 0.12],
      [88, 207, 169, 0.14],
      [13968, 31891, 24957, 0.13],
      [978, 3588, 2921, 0.08],
      [10175, 23926, 19006, 0.12],
      [2, 2, 1, 0.27],
    ],
    [
      [30541, 97740, 74172, 0.08],
      [13764, 47138, 35906, 0.06],
      [26725, 80185, 60646, 0.09],
      [2561, 4150, 3095, 0.18],
      [111, 234, 176, 0.16],
      [2, 12, 9, 0.05],
      [25110, 61972, 48377, 0.12],
      [10175, 23926, 19006, 0.12],
      [4787, 12147, 8638, 0.12],
      [2835, 6338, 4930, 0.14],
    ],
    [
      [524, 560, 400, 0.25],
      [129940, 234451, 169684, 0.16],
      [117237, 205811, 147670, 0.16],
      [129216, 232209, 167864, 0.16],
      [20, 54, 37, 0.1],
      [511, 1082, 875, 0.16],
      [31, 67, 39, 0.16],
      [2, 2, 1, 0.27],
      [2835, 6338, 4930, 0.14],
      [346, 774, 556, 0.15],
    ],
  ];
  let film_types = [
    [140, 27],
    [91, 45],
    [69, 27],
    [297, 57],
    [130, 40],
    [405, 0],
    [451, 60],
    [86, 14],
    [94, 0],
    [77, 21],
  ];
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

  //Initialize canvas and inner/outer radii of the chords
  const width = 1200,
    height = 1200,
    outerRadius = 465,
    innerRadius = outerRadius - 20;
  // for dropdowns
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
  const [film, setFilm] = useState("Combined Films");
  const [usStateStr, setusStateStr] = React.useState("California");
  const menu_filters = ["Combined Films", "Feature Films", "OTT Films"];
  const handleFilmChange = (event) => {
    setFilm(event.target.value);
  };
  const handleStateChange = (event) => {
    setusStateStr(event.target.value);
  };
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
    pie_data.map((item) => {
      let y = {};
      y["data"] = item["data"];
      y["value"] = item["value"];
      y["endAngle"] = Number(item["endAngle"] - 0.011);
      y["startAngle"] = item["startAngle"];
      y["padAngle"] = 0;
      y["index"] = item["index"];
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
    const chord_data = chord(matrix);

    const svg = d3.selectAll("svg");
    svg.selectAll("*").remove();
    const g = svg
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
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
      // .append("g")
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
            d.value
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
        .style("font-size", "22px")
        .style("font-weight", "normal");
    }

    // film type
    let film_chord = tweet_sentiment_angles(
      chord_data.groups,
      film_types,
      true
    );
    const film_group = g
      .append("g")
      .attr("class", "film_group")
      .selectAll("g")
      .data(film_chord)
      .enter()
      .append("g");
    if (film === "Combined Films") {
      console.log("inside if");
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

    // Logic for TweetCount

    // Logic for Tweet Count Sentiment
    let tweet_count_senti_groups = tweet_sentiment_angles(
      tweet_data,
      tweet_senti,
      false
    );
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
          console.log("ribbion");
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
  }, [film, usStateStr]);
  return (
    <div className="d-flex flex-column justify-content-center">
      <div className="d-flex flex-row justify-content-end m-4 p-4">
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
        <svg width="1300" height="1800">
          {/* <g className="groups" /> */}
        </svg>
      </div>
    </div>
  );
  //   <svg ref={svgRef} width="1300" height="1800"></svg>;
};
export default ChordChart;
