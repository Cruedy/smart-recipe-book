import urllib.request
import json
from ingredientSearch import searchIngredient
import re



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
            # Output result
            # for item in measured_ingredients:
            #     print(item)
            return measured_ingredients
    except Exception as error:
        print("Couldn't fetch ingredients", error)

# def allRecipeIngredients(ingredient):
#     names, links, images, ids = searchRecipe(ingredient)
#     fullRecipes = {}
#     for i in range(len(ids)):
#         fullRecipes[names[i]] = getIngredients(ids[i])
#     print(fullRecipes)


def getRecipeNutrion(ingredients):
    for i in ingredients:
        pattern = r"(?:\d+.*\s)?(?:tablespoons?|teaspoons?|ml|g|cm|cloves?)?\s*(.*)"
        




id = '52820'
ingredient = "chicken_breast"

print(getIngredients(id))