import { select } from "d3";
import * as d3 from "d3";
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const GeoChart = () => {
  const data = Object.assign(
    new Map(
      d3.csv("./maptemplate.csv").text(),
        ({ name, rate }) => [name, +rate]
      )
    )
    // { title: "Unemployment rate (%)" }
//   ;
  console.log(data)
  return <div></div>;
};
export default GeoChart;
