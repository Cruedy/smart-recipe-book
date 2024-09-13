import React, {useState} from 'react'

function SearchBars() {
  const [calorieMinValue, setCalorieMinValue] = useState('')
  const [calorieMaxValue, setCalorieMaxValue] = useState('')
  const [fatValue, setFatValue] = useState('')
  const [carbsValue, setCarbsValue] = useState('')
  const [proteinValue, setProteinValue] = useState('')
  const [ingredientValue, setIngredientValue] = useState('')

  const click = () => {
    alert(calorieMinValue)
    alert(calorieMaxValue)
    alert(fatValue)
    alert(carbsValue)
    alert(proteinValue)
  }

  const inputMinCal = event => {
    setCalorieMinValue(event.target.value)
  }
  const inputMaxCal = event => {
    setCalorieMaxValue(event.target.value)
  }
  const inputFat = event => {
    setFatValue(event.target.value)
  }
  const inputCarbs = event => {
    setCarbsValue(event.target.value)
  }
  const inputProtein = event => {
    setProteinValue(event.target.value)
  }
  const inputIngredient = event => {
    setIngredientValue(event.target.value)
  }
  return (
    <div>
      <input placeholder = "Min Calories..." onChange= {inputMinCal} value={calorieMinValue}/>
      <input placeholder = "Max Calories..." onChange= {inputMaxCal} value={calorieMaxValue}/>
      <input placeholder = "Max Fat..." onChange= {inputFat} value={fatValue}/>
      <input placeholder = "Max Carbs..." onChange= {inputCarbs} value={carbsValue}/>
      <input placeholder = "Min Protein..." onChange= {inputProtein} value={proteinValue}/>
      <br></br>
      <input placeholder = "Ingredient..." onChange= {inputIngredient} value={ingredientValue}/>
      <br></br>
      <button onClick = {click}>
        Click me
      </button>
    </div>
  )
}

export default SearchBars
