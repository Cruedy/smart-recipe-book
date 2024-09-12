import React, {useEffect, useState} from 'react';

const Filter = () => {
    const URL = "https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast";
    const URL_Base = "https://www.themealdb.com/meal/"

    const [recipeList, setRecipeList] = useState(" ");
    const [displayList, setDisplayList] = useState(" ");

    useEffect(() => {
        const fetchRecipes = async() => {
            try {
                const res = await fetch(URL);
                console.log('here');
                const data = await res.json();
                
                console.log(data.meals, "dataMeals");
                setRecipeList(data.meals);
                const listRecipes = recipeList.map(recipe => 
                    <li>
                        <a href={'https://www.themealdb.com/meal/'+ recipe.idMeal}>
                        <img src={recipe.strMealThumb}></img>
                        </a>
                        <p>{recipe.strMeal}</p>
                        
                    </li>
                )
                setDisplayList(listRecipes);
            } catch(error) {
                console.log("Couldn't fetch recipe", error);
            }
        }
        fetchRecipes()
    }, [])

    

  return (
    <div>
      <ul>{displayList}</ul>
    </div>
  )
}

export default Filter
