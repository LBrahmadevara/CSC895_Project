import React from "react";
import "./App.css";
import ChordChartValues from "./frontend/ChordChart/ChordChartValues";
import GeoChart from "./frontend/GeoChart/GeoChart";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";

function App() {
  const [value, setValue] = React.useState("one");

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <div className="App">
      <div className="main-title-vis d-flex justify-content-center">
        <h1><b>Exploratory Visualization of Movies and their Tweet Sentiment</b></h1>
      </div>
      <div className="tabs-div d-flex justify-content-center">
        <Tabs
          value={value}
          onChange={handleChange}
          textColor="secondary"
          indicatorColor="secondary"
          aria-label="secondary tabs example"
        >
          <Tab value="one" label="Chord" className="each-tab" />
          <Tab value="two" label="Choropleth" />
        </Tabs>
      </div>
      {value === "one" ? <div className="main-chord-chart"><ChordChartValues /></div>: <GeoChart />}
    </div>
  );
}

export default App;
