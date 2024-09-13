import json
from recipeSearch import *
from ingredientSearch import *

def create_recipe_json(filename):
    all_recipes = getAllRecipes()
    recipe_data = {}

    for recipe in all_recipes:
        idMeal = recipe[3]
        ingredients = getIngredients(idMeal)
        ingredient_details = {}
        for i in ingredients:
            ingredient_details[i] = searchIngredient(i)
        print("ingredient details", ingredient_details, recipe)
        calories = fat = carbs = protein = 0.0 
        max = 0.0
        for i in range(10):
            cal, f, car, pro= getRecipeNutrition(ingredients)
            if sum([calories, fat, carbs, protein]) > max:
                calories, fat, carbs, protein = cal, f, car, pro

        recipe_data[idMeal] = {
            'strMeal': recipe[0],
            'strMealThumb': recipe[2],
            'strMealLink': recipe[1],
            'calories': calories,
            'fat': fat,
            'carbs': carbs,
            'protein': protein,
            'ingredients': ingredient_details
        }

    # Write data to JSON file
    with open(filename, 'w') as json_file:
        json.dump(recipe_data, json_file, indent=4)

def fixNutritionFacts(file):
    try:
        with open(file, 'r') as json_file:
            recipes_data = json.load(json_file)
        for k in recipes_data.keys():
            recipe = recipes_data[k]
            ingredients = recipe.get('ingredients', {})  # Get the ingredients dictionary
            for ingredient_name, nutrition_fact in ingredients.items():
                if nutrition_fact is None:
                    # If the nutrition fact is None, search for the ingredient's nutrition facts
                    nutrition_facts = searchIngredient(ingredient_name)

                    # print(f"Found nutrition facts for {ingredient_name}: {nutrition_facts}")
                    
                    if nutrition_facts:
                        # Assuming the result from searchIngredient is a dictionary with the required nutrition data
                        ingredients[ingredient_name] = nutrition_facts
                        print("success: ", ingredients[ingredient_name])
                    else:
                        print(f"No nutrition facts found for {ingredient_name}")
        with open(file, 'w') as json_file:
            json.dump(recipes_data, json_file, indent=4)

        return recipes_data
    except FileNotFoundError:
        print("File not found.")
        return {}

print(fixNutritionFacts('recipes.json'))