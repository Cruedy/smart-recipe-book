import json
from recipeSearch import *
from ingredientSearch import *

'''
Description: Creates a json of all recipes, including the recipes id, name, image, link, calories, fat, carbs,
protein, and ingredients. Each ingredient in ingredients also has it's calorie, fat, carb, and protein information.
Parameters: filename - the name of the file that is created and writtten to
Return: None
''' 
def create_recipe_json(filename):
    all_recipes = getAllRecipes()
    recipe_data = {}

    for recipe in all_recipes:
        idMeal = recipe[3]
        ingredients = getIngredients(idMeal)
        ingredient_details = {}
        for i in ingredients:
            ingredient_details[i] = searchIngredient(i)
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

'''
Description: Checks each recipe in file, and fixes the nutrition facts of each ingredient using the Fat Secret API, which is
called in searchIngredient(ingredient_name) function. This function was written because the Fat Secret API has a rate limit,
which caused a problem when file was originally created.
Parameters: filename - the name of the file that is created and writtten to
Return: the recipe data from file
''' 
def fixNutritionFacts(file):
    print('in this function')
    try:
        with open(file, 'r') as json_file:
            recipes_data = json.load(json_file)
        for k in recipes_data.keys():
            print('id: ', k)
            recipe = recipes_data[k]
            ingredients = recipe.get('ingredients', {})  # Get the ingredients dictionary
            for ingredient_name, nutrition_fact in ingredients.items():
                if nutrition_fact == "":
                    print('nutrition fact:', ingredient_name)
                    print('item: ', k)
                    # If the nutrition fact is None, search for the ingredient's nutrition facts
                    nutrition_facts = searchIngredient(ingredient_name)
                    # print(f"Found nutrition facts for {ingredient_name}: {nutrition_facts}")
                    
                    if nutrition_facts:
                        # Assuming the result from searchIngredient is a dictionary with the required nutrition data
                        ingredients[ingredient_name] = nutrition_facts
                        print("success: ", ingredients[ingredient_name])
                        with open(file, 'w') as json_file:
                            json.dump(recipes_data, json_file, indent=4)
                    else:
                        print(f"No nutrition facts found for {ingredient_name}")

        return recipes_data
    except FileNotFoundError:
        print("File not found.")
        return {}

result = fixNutritionFacts('recipes.json')
print(result)

'''
Description: Sums up the calorie, fat, carb, and protein information from each ingredient to update each recipe's total 
calorie, fat, carb, and protein information in file.
Parameters: filename - the name of the file that is created and writtten to
Return: empty json if file isn't found
'''     
def fixTotalNutrition(file):
    try:
        with open(file, 'r') as json_file:
            recipes_data = json.load(json_file)
        for k in recipes_data.keys():
            recipe = recipes_data[k]
            calories = fat = carbs = protein = 0.0
            print("macros: ", calories, fat, carbs, protein)
            ingredients = recipe.get('ingredients', {}) 
            # print("ingredients: ", ingredients)
            for i in ingredients.keys():
                if ingredients[i] != "":
                    ingredient_nutrition = ingredients[i][i]
                    cal = ingredient_nutrition['calories']
                    fa = ingredient_nutrition['fat']
                    car = ingredient_nutrition['carbs']
                    pro = ingredient_nutrition['protein']
                    ingredient_cal = ingredient_fa = ingredient_car = ingredient_pro = ''
                    for c in cal:
                        if c.isdecimal() or c.isnumeric():
                            ingredient_cal += c
                    for f in fa:
                        if f.isdecimal() or f.isnumeric():
                            ingredient_fa += f
                    for c in car:
                        if c.isdecimal() or c.isnumeric():
                            ingredient_car += c
                    for p in pro:
                        if p.isdecimal() or p.isnumeric():
                            ingredient_pro += p
                    calories += float(ingredient_cal)
                    fat += float(ingredient_fa)
                    carbs += float(ingredient_car)
                    protein += float(ingredient_pro)
                else:
                    calories += 0.0
                    fat += 0.0
                    carbs += 0.0
                    protein += 0.0
            recipe['calories'] = calories
            recipe['fat'] = fat
            recipe['carbs'] = carbs
            recipe['protein'] = protein
            print("final macros: ", recipe['calories'], recipe['fat'], recipe['carbs'], recipe['protein'])
        with open(file, 'w') as json_file:
            json.dump(recipes_data, json_file, indent=4)
    except FileNotFoundError:
        print("File not found.")
        return {}
