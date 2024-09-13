import logo from './logo.svg';
import './App.css';
import Filter from './components/Filter';
import React, {useEffect, useState} from 'react';
import SearchBars from './components/SearchBars';

function App() {
  const [backend, setBackend] = useState(0);

  useEffect (() => {
    fetch("/api/route")
    .then(response => response.text())
    .then(data => setBackend(data))
    .catch(error => console.error('Error fetching data:', error));
  }, []);
  return (
    <div>
      <h1>The Smart Recipe Book</h1>
      <SearchBars></SearchBars>
      <Filter></Filter>
      <p>{backend}</p>
    </div>
  );
}

export default App;
