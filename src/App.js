import logo from './logo.svg';
import './App.css';
import Filter from './components/Filter';
import React, {useEffect, useState} from 'react';

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
      <Filter></Filter>
      <p>{backend}</p>
    </div>
  );
}

export default App;
