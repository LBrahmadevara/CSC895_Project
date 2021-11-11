import React from 'react';
import logo from './logo.svg';
import './App.css';
import DatabaseAPI from './frontend/DatabaseAPI';
import MoviesAPI from './frontend/MoviesAPI';
import Chart from './frontend/Chart';

function App() {
  return (
    <div className="App">
      {/* <MoviesAPI /> */}
      <Chart />
    </div>
  );
}

export default App;
