import React, {useEffect, useState} from 'react';


function Filter({ recipes }) {
    const listRecipes = recipes.map(recipe => (
        <li key={recipe.strMealLink}> 
            <a href={recipe.strMealLink}>
                <img src={recipe.strMealThumb} alt={recipe.strMeal} />
            </a>
            <p>{recipe.strMeal}</p>
        </li>
    ));
    console.log(recipes);
    return (
      <div>
        <ul>{listRecipes}</ul>
      </div>
    );
}

export default Filter
