import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import * as d3 from "d3";
import { select, scaleBand, scaleLinear, axisBottom, axisLeft, svg } from "d3";

const Chart = () => {
  const colors = [
    "#c4c4c4",
    "#69b40f",
    "#ec1d25",
    "#c8125c",
    "#008fc8",
    "#10218b",
    "#134b24",
    "#737373",
    "#c3c370",
    "#f3ae5d",
  ];
  const data = [
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
  const names = [
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
  const totalDataSum = 2533;
  const sentiment = [];
  const svgRef = useRef();
  const formatValue = d3.format(".001~%");
  // console.log(formatValue(99))
  // const innerRadius = 506;
  // const outerRadius = 516;
  // const height = 1200;
  // const width = 1200;
  const innerRadius = 256;
  const outerRadius = 270;
  const height = 720;
  const width = 650;

  useEffect(() => {
    let svg = d3
      .select("#my_dataviz")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      // .append("g")
      // .attr("transform", `translate(${width / 2},${height / 2})`);
      .attr("viewBox", [-width / 2, -height / 2, width, height + 20]);

    const chord = d3
      .chord()
      .padAngle(15 / innerRadius)
      .sortSubgroups(d3.descending)
      .sortChords(d3.descending);

    const chords = chord(data);
    console.log(chords.groups);

    const tickStep = d3.tickStep(0, d3.sum(data.flat()), 5);
    console.log(d3.sum(data.flat()));

    const ribbon = d3
      .ribbon()
      .radius(innerRadius - 6)
      .padAngle(3 / innerRadius);

    const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
    console.log("arc: ", arc);

    const color = d3.scaleOrdinal(names, colors);

    const group = svg
      .append("g")
      .attr("font-size", 10)
      .attr("font-family", "sans-serif")
      .selectAll("g")
      .data(chords.groups)
      .join("g");

    group
      .append("path")
      .attr("fill", (d) => color(names[d.index]))
      .attr("d", arc);

    // group.append("title").text(
    //   (d) => `${names[d.index]}
    //     ${formatValue(d.value)}`
    // );
    group.append("title").text(
      (d) => `${names[d.index]}
        ${((d.value / totalDataSum) * 100).toFixed(2)}%`
    );

    function ticks({ startAngle, endAngle, value }) {
      const k = (endAngle - startAngle) / value;
      return d3.range(0, value, tickStep).map((value) => {
        return { value, angle: value * k + startAngle };
      });
    }

    const groupTick = group
      .append("g")
      .selectAll("g")
      .data(ticks)
      .join("g")
      .attr(
        "transform",
        (d) =>
          `rotate(${
            (d.angle * 180) / Math.PI - 90
          }) translate(${outerRadius},0)`
      );

    groupTick.append("line").attr("stroke", "currentColor").attr("x2", 6);

    groupTick
      .append("text")
      .attr("x", 8)
      .attr("dy", "0.35em")
      .attr("transform", (d) =>
        d.angle > Math.PI ? "rotate(180) translate(-16)" : null
      )
      .attr("text-anchor", (d) => (d.angle > Math.PI ? "end" : null));
    // .text((d) => d.value*0.01);

    group
      .select("text")
      .attr("font-weight", "bold")
      .attr("font-size", "15")
      .text(function (d) {
        return names[d.index];
      });

    svg
      .append("g")
      .attr("fill-opacity", 0.8)
      .selectAll("path")
      .data(chords)
      .join("path")
      .style("mix-blend-mode", "multiply")
      .attr("fill", (d) => color(names[d.source.index]))
      .attr("d", ribbon)
      .append("title")
      .text((d) =>
        d.source.index === d.target.index
          ? `${names[d.source.index]} have ${d.source.value} movies`
          : `${names[d.target.index]} and ${names[d.source.index]} have ${
              d.source.value + d.target.value
            } movies`
      );
  });
  return (
    <div>
      <div id="my_dataviz"></div>
    </div>
  );
};
export default Chart;
