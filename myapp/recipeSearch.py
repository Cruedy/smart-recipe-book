import urllib.request
import json
from ingredientSearch import searchIngredient
import re
import string
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# recipes = getAllRecipes()
# print(recipes)
    

    # recipes = []
    # url_base = "https://www.themealdb.com/api/json/v1/1/search.php?f="
    # for n in string.ascii_lowercase:
    #     url = url_base + n
    #     try:
    #         with urllib.request.urlopen(url) as response:
    #             data = json.loads(response.read().decode())
    #             if data["meals"] != None:
    #                 meal = []
    #                 for d in data["meals"]:
    #                     # print("meal: ", d)
    #                     meal.append(d['strMeal'])
    #                     meal.append("https://www.themealdb.com/meal/"+d['idMeal'])
    #                     meal.append(d['strMealThumb'])
    #                     meal.append(d['idMeal'])
    #                     recipes.append(meal) 
    #                     # print("meal1 :", len(meal))
    #                     meal = []
    #     except Exception as error:
    #         print("Couldn't fetch recipe", error)
    # return recipes 

# print(getAllRecipes()) 

def searchRecipe(ingredient):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=" + ingredient
    url_base = "https://www.themealdb.com/meal/"

    recipeList = []
    displayList = []
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
                    # print(f"Recipe: {item[2]}, Link: {item[0]}, Image: {item[1]}")
                return names, links, images, ids
            else:
                print("No meals found.")
    except Exception as error:
        print("Couldn't fetch recipe", error)

def getIngredients(id):
    ingredient_url = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i=' + id
    try:
        # Open the URL and fetch the data
        with urllib.request.urlopen(ingredient_url) as response:
            data = json.loads(response.read().decode())
            # print(data['meals'][0])

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

def getRecipeNutrition(ingredients):
    calories = 0.0
    fat = 0.0
    carbs = 0.0
    protein = 0.0
    for i in ingredients:
        # print("ingredient: ", i)
        # print(type(i))
        nutrition_facts = searchIngredient(i)
        # print("nutrition_facts: ", nutrition_facts, i)
        # print("nutrition_facts", nutrition_facts)
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



# id = '52772'
# ingredient = "chicken_breast"
# names, links, images, ids  = searchRecipe(ingredient)
# ingredients, name = getIngredients(ids[6], names[6])
ingredients = ['1 tsp  Sesame Seed Oil', '3 finely chopped Carrots', '3 finely chopped Celery', '6 chopped Spring Onions', '1 Packet Wonton Skin']
print(sum(getRecipeNutrition(ingredients)))