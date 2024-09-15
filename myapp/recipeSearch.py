import urllib.request
import json
from ingredientSearch import searchIngredient
import re
import string
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

'''
Description: Gets all recipes in the mealdb api
Parameters: None
Return: all recipes in the mealdb api
''' 
def getAllRecipes():
    recipes = []
    url_base = "https://www.themealdb.com/api/json/v1/1/search.php?f="

    def fetch_recipes(letter):
        url = url_base + letter
        meal = []
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                if data["meals"] != None:
                    for d in data["meals"]:
                        meal.append([d['strMeal'], "https://www.themealdb.com/meal/"+d['idMeal'], d['strMealThumb'], d['idMeal']])
        except Exception as error:
            print(f"Couldn't fetch recipes for {letter}: ", error)
        return meal

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust the worker count based on performance
        futures = [executor.submit(fetch_recipes, letter) for letter in string.ascii_lowercase]

        for future in as_completed(futures):
            result = future.result()
            recipes.extend(result)

    return recipes

'''
Description: searches for a recipe using the mealdb api by ingredient
Parameters: ingredient - ingredient that qualifies the recipes
Return: the names, links, images, and ids of all recipes that contain ingredient
''' 
def searchRecipe(ingredient):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=" + ingredient
    url_base = "https://www.themealdb.com/meal/"

    try:
        # Open the URL and fetch the data
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

            # Process the meal data
            if 'meals' in data:
                recipe_list = data['meals']

                # Create display list
                display_list = []
                for recipe in recipe_list:
                    recipe_id = recipe['idMeal']
                    recipe_link = f"{url_base}{recipe['idMeal']}"
                    recipe_img = recipe['strMealThumb']
                    recipe_name = recipe['strMeal']
                    # Append tuple with recipe info to the display_list
                    display_list.append((recipe_link, recipe_img, recipe_name, recipe_id))
                
                names = []
                links = []
                images = []
                ids = []

                # Print the display list for verification
                for item in display_list:
                    names.append(item[2])
                    links.append(item[0])
                    images.append(item[1])
                    ids.append(item[3])
                return names, links, images, ids
            else:
                print("No meals found.")
    except Exception as error:
        print("Couldn't fetch recipe", error)

'''
Description: gets all ingredients in a recipe
Parameters: id - id value of recipe
Return: a list of all ingredients in recipe
''' 
def getIngredients(id):
    ingredient_url = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i=' + id
    try:
        # Open the URL and fetch the data
        with urllib.request.urlopen(ingredient_url) as response:
            data = json.loads(response.read().decode())

            ingredient_keys = [key for key in data['meals'][0] if key.startswith('strIngredient')]
            measure_keys = [key for key in data['meals'][0] if key.startswith('strMeasure')]

            ingredient_keys.sort()
            measure_keys.sort()
            measured_ingredients = []
            meal_data = data['meals'][0]
            for ingredient_key, measure_key in zip(ingredient_keys, measure_keys):
                ingredient = meal_data.get(ingredient_key)
                measure = meal_data.get(measure_key)
                
                if ingredient and measure:
                    measured_ingredients.append(f"{measure} {ingredient}")
                elif ingredient:  # If there's an ingredient but no measure
                    measured_ingredients.append(f"{ingredient}")

            return measured_ingredients
    except Exception as error:
        print("Couldn't fetch ingredients", error)
    pass

'''
Description: given a list of ingredients, uses searchIngredient(i) to get the calorie, fat, carb, and protein values of 
the recipe
Parameters: ingredients - a list of ingredients
Return: the total calories, fat, carbs, and protein in a list of ingredients
''' 
def getRecipeNutrition(ingredients):
    calories = 0.0
    fat = 0.0
    carbs = 0.0
    protein = 0.0
    for i in ingredients:
        nutrition_facts = searchIngredient(i)
        if nutrition_facts != None:
            cal_val = list(nutrition_facts.values())[0]['calories']
            cal_num = ''
            for c in cal_val:
                if not c.isalpha():
                    cal_num += c
            fat_val = list(nutrition_facts.values())[0]['fat']
            fat_num = ''
            for f in fat_val:
                if not f.isalpha():
                    fat_num += f
            carb_val = list(nutrition_facts.values())[0]['carbs']
            carb_num = ''
            for ca in carb_val:
                if not ca.isalpha():
                    carb_num += ca
            pro_val = list(nutrition_facts.values())[0]['protein']
            pro_num = ''
            for p in pro_val:
                if not p.isalpha():
                    pro_num += p
            calories += float(cal_num)
            fat += float(fat_num)
            carbs += float(carb_num)
            protein += float(pro_num)
    return calories, fat, carbs, protein