// Reference from- https://github.com/muratkemaldar/using-react-hooks-with-d3

import React, { useRef, useEffect, useState } from "react";
import { select, geoPath, scaleLinear, geoAlbersUsa } from "d3";
import data from "./gz_2010_us_040_00_500k.json";
import "./GeoChart.css";
import * as d3 from "d3";
// import {legend} from "d3-color-legend"
import legend from "./legend.png";

const GeoChart = () => {
  const svgRef = useRef();
  const wrapperRef = useRef();
  const [selectedState, setSelectedState] = useState(null);
  let salesData = {
    Alabama: 28559,
    Alaska: 9584,
    Arizona: 62265,
    Arkansas: 13642,
    California: 448679,
    Colorado: 50666,
    Connecticut: 26399,
    Delaware: 3625,
    "District of Columbia": 30347,
    Florida: 204114,
    Georgia: 79700,
    Hawaii: 15051,
    Idaho: 7901,
    Illinois: 112639,
    Indiana: 49852,
    Iowa: 18149,
    Kansas: 16645,
    Kentucky: 24268,
    Louisiana: 41443,
    Maine: 6275,
    Maryland: 58947,
    Massachusetts: 68100,
    Michigan: 58158,
    Minnesota: 35739,
    Mississippi: 10980,
    Missouri: 40936,
    Montana: 30572,
    Nebraska: 13638,
    Nevada: 44617,
    "New Hampshire": 7017,
    "New Jersey": 76211,
    "New Mexico": 12366,
    "New York": 252243,
    "North Carolina": 118004,
    "North Dakota": 4321,
    Ohio: 89054,
    Oklahoma: 39804,
    Oregon: 39241,
    Pennsylvania: 86715,
    "Rhode Island": 9979,
    "South Carolina": 27200,
    "South Dakota": 30593,
    Tennessee: 55256,
    Texas: 321228,
    Utah: 22574,
    Vermont: 2456,
    Virginia: 63163,
    Washington: 67277,
    "West Virginia": 7479,
    Wisconsin: 25762,
    Wyoming: 1898,
  };

  let tweet_senti = {
    Alabama: [8270, 19704, 14454],
    Alaska: [2262, 7179, 5819],
    Arizona: [17533, 43504, 32612],
    Arkansas: [3812, 9560, 7164],
    California: [129768, 310644, 228437],
    Colorado: [14142, 35658, 26561],
    Connecticut: [7824, 18105, 13221],
    Delaware: [877, 2657, 1821],
    "District of Columbia": [8019, 21820, 15698],
    Florida: [57208, 143331, 109475],
    Georgia: [21235, 56953, 43115],
    Hawaii: [4359, 10432, 7880],
    Idaho: [2282, 5479, 4064],
    Illinois: [32466, 78167, 57069],
    Indiana: [14517, 34382, 25223],
    Iowa: [5507, 12356, 9048],
    Kansas: [5075, 11325, 8115],
    Kentucky: [7183, 16678, 12113],
    Louisiana: [10752, 29836, 22618],
    Maine: [1864, 4306, 3064],
    Maryland: [16103, 41565, 31119],
    Massachusetts: [20029, 46833, 33708],
    Michigan: [16621, 40460, 29852],
    Minnesota: [10635, 24493, 17450],
    Mississippi: [3175, 7581, 5677],
    Missouri: [11863, 28311, 20701],
    Montana: [1018, 2499, 1720],
    Nebraska: [4076, 9350, 6562],
    Nevada: [13083, 30645, 22685],
    "New Hampshire": [2003, 4905, 3574],
    "New Jersey": [20883, 53854, 39994],
    "New Mexico": [3312, 8840, 6228],
    "New York": [68887, 178947, 126031],
    "North Carolina": [30479, 85970, 68401],
    "North Dakota": [1478, 2773, 1908],
    Ohio: [26180, 61197, 44690],
    Oklahoma: [11771, 27446, 20573],
    Oregon: [10683, 27484, 20667],
    Pennsylvania: [24200, 60809, 44922],
    "Rhode Island": [2926, 6853, 5055],
    "South Carolina": [7513, 19251, 14613],
    "South Dakota": [996, 2528, 1839],
    Tennessee: [16298, 37957, 27687],
    Texas: [94997, 220404, 164576],
    Utah: [6599, 15530, 11174],
    Vermont: [690, 1728, 1259],
    Virginia: [18061, 43901, 32207],
    Washington: [19334, 46772, 33552],
    "West Virginia": [2277, 5073, 3561],
    Wisconsin: [7525, 17743, 12939],
    Wyoming: [562, 1295, 963],
  };

  let movies_count = {
    Alabama: 619,
    Alaska: 372,
    Arizona: 782,
    Arkansas: 508,
    California: 1301,
    Colorado: 724,
    Connecticut: 622,
    Delaware: 343,
    "District of Columbia": 645,
    Florida: 999,
    Georgia: 790,
    Hawaii: 518,
    Idaho: 438,
    Illinois: 894,
    Indiana: 720,
    Iowa: 544,
    Kansas: 544,
    Kentucky: 626,
    Louisiana: 648,
    Maine: 408,
    Maryland: 761,
    Massachusetts: 817,
    Michigan: 764,
    Minnesota: 676,
    Mississippi: 457,
    Missouri: 708,
    Montana: 326,
    Nebraska: 508,
    Nevada: 753,
    "New Hampshire": 427,
    "New Jersey": 815,
    "New Mexico": 502,
    "New York": 1134,
    "North Carolina": 774,
    "North Dakota": 378,
    Ohio: 814,
    Oklahoma: 622,
    Oregon: 674,
    Pennsylvania: 824,
    "Rhode Island": 478,
    "South Carolina": 609,
    "South Dakota": 320,
    Tennessee: 724,
    Texas: 1085,
    Utah: 621,
    Vermont: 311,
    Virginia: 794,
    Washington: 789,
    "West Virginia": 420,
    Wisconsin: 633,
    Wyoming: 264,
  };
  let avg_senti = {
    Alabama: 0.12,
    Alaska: 0.1,
    Arizona: 0.11,
    Arkansas: 0.12,
    California: 0.12,
    Colorado: 0.12,
    Connecticut: 0.13,
    Delaware: 0.11,
    "District of Columbia": 0.11,
    Florida: 0.12,
    Georgia: 0.11,
    Hawaii: 0.13,
    Idaho: 0.12,
    Illinois: 0.12,
    Indiana: 0.13,
    Iowa: 0.13,
    Kansas: 0.13,
    Kentucky: 0.13,
    Louisiana: 0.11,
    Maine: 0.13,
    Maryland: 0.11,
    Massachusetts: 0.13,
    Michigan: 0.12,
    Minnesota: 0.13,
    Mississippi: 0.13,
    Missouri: 0.12,
    Montana: 0.12,
    Nebraska: 0.13,
    Nevada: 0.12,
    "New Hampshire": 0.13,
    "New Jersey": 0.12,
    "New Mexico": 0.11,
    "New York": 0.12,
    "North Carolina": 0.11,
    "North Dakota": 0.16,
    Ohio: 0.13,
    Oklahoma: 0.13,
    Oregon: 0.11,
    Pennsylvania: 0.12,
    "Rhode Island": 0.12,
    "South Carolina": 0.12,
    "South Dakota": 0.12,
    Tennessee: 0.13,
    Texas: 0.12,
    Utah: 0.12,
    Vermont: 0.12,
    Virginia: 0.12,
    Washington: 0.12,
    "West Virginia": 0.13,
    Wisconsin: 0.12,
    Wyoming: 0.12,
  };
  const width = 1600;
  const height = 1300;

  useEffect(() => {
    const svg = select(svgRef.current);
    svg
      .select("body")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    const colorScale = scaleLinear()
      .domain([-50000, 448679])
      .range(["white", "red"]);
    const projection = geoAlbersUsa()
      .fitSize([1600, 800], selectedState || data)
      .precision(100);
    const pathGenerator = geoPath().projection(projection);
    svg
      .selectAll(".state")
      .data(data.features)
      .join("path")
      .attr("class", "state")
      .on("mouseenter", (event, value) => {
        svg
          .selectAll(".tooltip")
          .data([value])
          .join((enter) => enter.append("text"))
          .attr("class", "tooltip")
          .transition()
          .style("opacity", 2);
      })
      .on("mousemove", (event, value) => {
        console.log(value);
        svg
          .select(".tooltip")
          .html(
            (d) => `<tspan x=${event.offsetX + 50}px y=${
              event.offsetY - 1
            }px>State: ${d["properties"]["NAME"]} </tspan>
          <tspan x=${event.offsetX + 50}px y=${
              event.offsetY + 31
            // }px>Number of Tweets: ${salesData[d["properties"]["NAME"]]}</tspan>
            // <tspan x=${event.offsetX + 50}px y=${
            //   event.offsetY + 61
          }px>Number of Tweets: ${tweet_senti[d["properties"]["NAME"]][0]+tweet_senti[d["properties"]["NAME"]][1]+tweet_senti[d["properties"]["NAME"]][2]}</tspan>
          <tspan x=${event.offsetX + 50}px y=${
            event.offsetY + 61
            }px>Number of Movies: ${
              movies_count[d["properties"]["NAME"]]
            } </tspan><tspan x=${event.offsetX + 50}px y=${
              event.offsetY + 91
            }px>Number of +ve Tweets: ${
              tweet_senti[d["properties"]["NAME"]][0]
            } </tspan><tspan x=${event.offsetX + 50}px y=${
              event.offsetY + 121
            }px>Number of Neutral Tweets: ${
              tweet_senti[d["properties"]["NAME"]][1]
            } </tspan><tspan x=${event.offsetX + 50}px y=${
              event.offsetY + 151
            }px>Number of -ve Tweets: ${
              tweet_senti[d["properties"]["NAME"]][2]
            } </tspan><tspan x=${event.offsetX + 50}px y=${
              event.offsetY + 181
            }px>Average Tweet Sentiment: ${
              avg_senti[d["properties"]["NAME"]]
            } </tspan>`
          )
          .attr("x", event.offsetX + 50 + "px")
          .attr("y", event.offsetY - 1 + "px");
      })
      .on("mouseleave", () => svg.selectAll(".tooltip").remove())
      .transition()
      .duration(1000)
      .attr("fill", (feature) =>
        colorScale(salesData[feature["properties"]["NAME"]]))
      .attr("d", (feature) => pathGenerator(feature));

    // svg
    //   .append("g")
    //   .attr("transform", "translate(150,50)")
    //   .attr("font-size", "35px")
    //   .append("text")
    //   .text("Tweet sentiment for the movies for all the states in the USA")
    //   .attr("class", "title");
  }, [selectedState]);

  return (
    <div className="d-flex flex-column justify-content-center geo-main">
      <div className="d-flex justify-content-center geo-title">
        Tweet Strength across all states in the United States
      </div>
      <div className="d-flex justify-content-end pt-4 ">
        <img
          src={legend}
          target="legend"
          className="img-thumbnail img-legend"
        />
      </div>
      {/* <svg
        ref={svgRef}
        style={{ width: 1000, height: 500, overflow: "visible" }}
      ></svg> */}
      <svg
        ref={svgRef}
        style={{ width: width, height: height, overflow: "visible" }}
      ></svg>
      {/* </div> */}
    </div>
  );
};

export default GeoChart;
