from flask import Flask, request, jsonify
from flask_cors import CORS 
from recipeSearch import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from rateLimitMonitor import RateLimitMonitor

app = Flask(__name__)
CORS(app)

rate_monitor = RateLimitMonitor()

@app.route('/api/route', methods=['POST'])
def returnFoodList():
    data = request.get_json()
    minCalories = int(data.get('minCalories', 0))
    maxCalories = int(data.get('maxCalories', 0))
    maxFat = int(data.get('maxFat', 0))
    maxCarbs = int(data.get('maxCarbs', 0))
    minProtein = int(data.get('minProtein', 0))
    ingredient = data.get('ingredient', '')
    ingredient_recipes = fromIngredient(ingredient)
    resulting_recipes = []

    with open('recipes.json', 'r') as json_file:
        recipes_data = json.load(json_file)
        for i in ingredient_recipes:
            recipe_id = i[3]
            recipe_info = recipes_data[recipe_id]

            calories = recipe_info['calories']
            # print("calories: ", calories)
            fat = recipe_info['fat']
            carbs = recipe_info['carbs']
            protein = recipe_info['protein']
            if (minCalories == 0 or calories >= minCalories) and \
                (maxCalories == 0 or calories <= maxCalories) and \
                (maxFat == 0 or fat <= maxFat) and \
                (maxCarbs == 0 or carbs <= maxCarbs) and \
                (minProtein == 0 or protein >= minProtein):
                resulting_recipes.append(recipe_info)
    return jsonify(resulting_recipes)

# helper function     
def fromIngredient(ingredient):
    names, links, images, ids = searchRecipe(ingredient)
    recipes = []
    for n in range(len(names)):
        meal = []
        meal.append(names[n])
        meal.append(links[n])
        meal.append(images[n])
        meal.append(ids[n])
        recipes.append(meal)
    return recipes
