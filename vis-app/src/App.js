import React from 'react';
import logo from './logo.svg';
import './App.css';
import DatabaseAPI from './frontend/DatabaseAPI';
import MoviesAPI from './frontend/MoviesAPI';

function App() {
  return (
    <div className="App">
      <MoviesAPI />
    </div>
  );
}

export default App;
