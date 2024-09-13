import React, {useState} from 'react'

function SearchBars({ onSearch }) {
  const [calorieMinValue, setCalorieMinValue] = useState(0)
  const [calorieMaxValue, setCalorieMaxValue] = useState(0)
  const [fatValue, setFatValue] = useState(0)
  const [carbsValue, setCarbsValue] = useState(0)
  const [proteinValue, setProteinValue] = useState(0)
  const [ingredientValue, setIngredientValue] = useState('')

  const click = async() => {
    const searchData = {
      minCalories: calorieMinValue,
      maxCalories: calorieMaxValue,
      maxFat: fatValue,
      maxCarbs: carbsValue,
      minProtein: proteinValue,
      ingredient: ingredientValue
    }
    onSearch(searchData);
  }

  // const inputMinCal = event => {
  //   setCalorieMinValue(event.target.value)
  // }
  // const inputMaxCal = event => {
  //   setCalorieMaxValue(event.target.value)
  // }
  // const inputFat = event => {
  //   setFatValue(event.target.value)
  // }
  // const inputCarbs = event => {
  //   setCarbsValue(event.target.value)
  // }
  // const inputProtein = event => {
  //   setProteinValue(event.target.value)
  // }
  // const inputIngredient = event => {
  //   setIngredientValue(event.target.value)
  // }
  return (
    <div>
      <input placeholder="Min Calories..." onChange={e => setCalorieMinValue(e.target.value)} value={calorieMinValue} />
      <input placeholder="Max Calories..." onChange={e => setCalorieMaxValue(e.target.value)} value={calorieMaxValue} />
      <input placeholder="Max Fat..." onChange={e => setFatValue(e.target.value)} value={fatValue} />
      <input placeholder="Max Carbs..." onChange={e => setCarbsValue(e.target.value)} value={carbsValue} />
      <input placeholder="Min Protein..." onChange={e => setProteinValue(e.target.value)} value={proteinValue} />
      <br></br>
      <input placeholder="Ingredient..." onChange={e => setIngredientValue(e.target.value)} value={ingredientValue} />
      <br></br>
      <button onClick = {click}>
        Click me
      </button>
    </div>
  )
}

export default SearchBars
