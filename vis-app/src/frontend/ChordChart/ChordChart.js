import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";

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
    "rgb(76 164 187)",
    "rgb(67 76 133)",
    "rgb(77 120 90)",
    "#737373",
    "#c3c370",
    "#f3ae5d",
  ];
  const senti_colors = ["green", "#36369f", "red"];
  const film_colors = ["red", "black"];

  let matrix = props.matrix;
  let label_movies_count_combined = props.label_movies_count_combined;
  let label_movies_count = props.label_movies_count;
  let ribbon_movies_count = props.ribbon_movies_count;
  let ribbon_tweet_count = props.ribbon_tweet_count;
  let ribbon_avg_senti = props.ribbon_avg_senti;
  let ribbon_senti = props.ribbon_senti;
  let tweet_count_for_last_circle = props.tweet_count_for_last_circle;
  let tweet_senti_for_last_circle = props.tweet_senti_for_last_circle;
  let movie_type = props.movie_type;

  //Initialize canvas and inner/outer radii of the chords
  const width = 1200,
    height = 1200,
    outerRadius = 550,
    innerRadius = outerRadius - 20;

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
      y["index"] = ind;
      y["value"] = item["value"];
      pie_data_with_padangle.push(y);
    });
    return pie_data_with_padangle;
  };

  useEffect(async () => {
    let totalDataSum = d3.sum(label_movies_count_combined);
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
        film_group
          .filter((d) => d.index !== i.index)
          .transition()
          .style("opacity", opacity);
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
    let chord_data = chord(matrix);

    const svg = d3.selectAll("svg");
    svg.selectAll("*").remove();
    const g = svg
      .append("g")
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
            label_movies_count_combined[d.index]
          } movies(${(
            (label_movies_count_combined[d.index] / totalDataSum) *
            100
          ).toFixed(2)}%) \nNumber of Feature Films: ${
            label_movies_count[d.index][0]
          }(${((label_movies_count[d.index][0]*100)/label_movies_count_combined[d.index]).toFixed(2)
          }%) \nNumber of OTT Films: ${label_movies_count[d.index][1]
          }(${((label_movies_count[d.index][1]*100)/label_movies_count_combined[d.index]).toFixed(2)}%)`
      );
    if (movie_type !== "Combined Films") {
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

    // 2nd circle
    let film_chord = tweet_sentiment_angles(
      chord_data.groups,
      label_movies_count,
      true
    );
    const film_group = g
      .append("g")
      .attr("class", "film_group")
      .selectAll("g")
      .data(film_chord)
      .enter()
      .append("g");

    if (movie_type === "Combined Films") {
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
    // 2nd circle

    // 3rd circle
    let tweet_data = pie_data_padangle(tweet_count_for_last_circle);
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
    // 3rd circle

    // 4th circle
    let tweet_count_senti_groups = tweet_sentiment_angles(
      tweet_data,
      tweet_senti_for_last_circle,
      false
    );
    console.log(tweet_count_senti_groups);
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
          tweet_count_for_last_circle[d["index"]]
        } (${(
          (tweet_count_for_last_circle[d["index"]] /
            d3.sum(tweet_count_for_last_circle)) *
          100
        ).toFixed(2)}%) \nNumber of +ve Tweets: ${
          tweet_senti_for_last_circle[d["index"]][0]
        } \nNumber of Neutral Tweets: ${
          tweet_senti_for_last_circle[d["index"]][1]
        }  \nNumber of -ve Tweets: ${
          tweet_senti_for_last_circle[d["index"]][2]
        } \nAverage Tweets Sentiment: ${
          tweet_senti_for_last_circle[d["index"]][3]
        }`;
      });
    // 4th circle

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
        group
          .filter((d) => {
            return !(d.index === i.source.index || d.index === i.target.index);
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
        film_group
          .filter((d) => {
            return !(d.index === i.source.index || d.index === i.target.index);
          })
          .transition()
          .style("opacity", opacity);
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
        ? `${genres[d.source.index]} has ${
            ribbon_movies_count[d.source.index][d.target.index]
          } movies \nand ${
            ribbon_tweet_count[d.source.index][d.target.index]
          } Tweets \nNumber of +ve Tweets: ${
            ribbon_senti[d.source.index][d.target.index][0]
          }  \nNumber of Nuetral Tweets: ${
            ribbon_senti[d.source.index][d.target.index][1]
          } \nNumber of -ve Tweets: ${
            ribbon_senti[d.source.index][d.target.index][2]
          } \nAverage Tweets Sentiment: ${
            ribbon_avg_senti[d.source.index][d.target.index]
          }`
        : `${genres[d.target.index]} and ${genres[d.source.index]} have \n${
            ribbon_movies_count[d.source.index][d.target.index]
          } movies and ${
            ribbon_tweet_count[d.source.index][d.target.index]
          } Tweets \nNumber of +ve Tweets: ${
            ribbon_senti[d.source.index][d.target.index][0]
          }  \nNumber of Nuetral Tweets: ${
            ribbon_senti[d.source.index][d.target.index][1]
          } \nNumber of -ve Tweets: ${
            ribbon_senti[d.source.index][d.target.index][2]
          } \nAverage Tweets Sentiment: ${
            ribbon_avg_senti[d.source.index][d.target.index]
          }`;
    });
  });
  return <svg ref={svgRef} width="1300" height="1800"></svg>;
};
export default ChordChart;
