import logo from './logo.svg';
import './App.css';
import Filter from './components/Filter';
import React, {useEffect, useState} from 'react';
import SearchBars from './components/SearchBars';

function App() {
  const [backend, setBackend] = useState(0);
  const [recipes, setRecipes] = useState([]);

  const handleSearch = async (searchData) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData),
      });
      const data = await response.json();
      setRecipes(data); // Update the state with the fetched recipes
    } catch (error) {
      console.error("Error fetching recipes: ", error);
    }
  };

  // useEffect (() => {
  //   fetch("/api/route")
  //   .then(response => response.text())
  //   .then(data => setBackend(data))
  //   .catch(error => console.error('Error fetching data:', error));
  // }, []);
  return (
    <div>
      <h1>The Smart Recipe Book</h1>
      <SearchBars onSearch={handleSearch}></SearchBars>
      <Filter recipes={recipes}></Filter>
    </div>
  );
}

export default App;
