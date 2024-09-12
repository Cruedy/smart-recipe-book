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

def getIngredients(id, name):
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
            return measured_ingredients, name
    except Exception as error:
        print("Couldn't fetch ingredients", error)

# def allRecipeIngredients(ingredient):
#     names, links, images, ids = searchRecipe(ingredient)
#     fullRecipes = {}
#     for i in range(len(ids)):
#         fullRecipes[names[i]] = getIngredients(ids[i])
#     print(fullRecipes)


def getRecipeNutrition(ingredients):
    calories = 0.0
    fat = 0.0
    carbs = 0.0
    protein = 0.0
    for i in ingredients:
        nutrition_facts = searchIngredient(i)
        # print(i)
        # print("nutrition facts", nutrition_facts)
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
        

    #     pattern = r"(.+?(?:tablespoons?|teaspoons?|ml|g|cm|cloves?|oz|slices?|pieces?|pinches?|cups?|pounds?)\s*)(.*)"
    
    #     # Use re.search to find the key ingredient(s)
    #     match = re.search(pattern, i)
    
    #     if match:
    #         # Group 1 is the quantity and unit, group 2 is the ingredient
    #         quantity = match.group(1).strip()
    #         ingredient = match.group(2).strip()
    #         clean_quantity = quantity
    #         for i, char in enumerate(quantity):
    #             if char == '(':
    #                 clean_quantity = quantity[i+1:]
    #                 break
    #         clean_ingredient = re.sub(r'[^a-zA-Z\s]', '', ingredient)
    #         for i, char in enumerate(clean_ingredient):
    #             if char.isalpha():
    #                 clean_ingredient = clean_ingredient[i:]
    #                 break
    #         ingredient_amounts.append([clean_quantity, clean_ingredient])
    # # the amount of each ingredient in the recipe
    # print(ingredient_amounts)
    # for n in ingredient_amounts:
    #     calories = ''
    #     protein = ''
    #     carbs = ''
    #     fat = ''
    #     # print(n[0])
    #     ingredient_num = ''
    #     ingredient_unit = ''
        
    #     for i, char in enumerate(n[0]):
    #         if char.isnumeric():
    #             ingredient_num += char
    #         if char.isalpha():
    #             ingredient_unit += char
    #     print('n1', n[1])
    #     nutrition_amount = searchIngredient(n[1])[n[1]]['amount']
    #     nutrition_num = ''
    #     nutrition_unit = ''
    #     for i, char in enumerate(nutrition_amount):
    #         if char.isnumeric():
    #             nutrition_num += char
    #         if char.isalpha():
    #             nutrition_unit += char
    #     if(ingredient_unit[len(ingredient_unit)-1] == 's'):
    #         ingredient_unit = ingredient_unit[:len(ingredient_unit)-1]
    #     if(nutrition_unit[len(nutrition_unit)-1] == 's'):
    #         nutrition_unit = nutrition_unit[:len(nutrition_unit)-1]
    #     print('nutrition_num: ', nutrition_num)
    #     print('nutrition_unit: ', nutrition_unit)
    #     print('ingredient_num: ', ingredient_num)
    #     print('ingredient_unit: ', ingredient_unit)
    #     print(" ")
    #     # you want the nutrition amount to match the ingredient amount
    #     def getMultiplier(nutrition_num, nutrition_unit, ingredient_num, ingredient_unit):
    #         print('')

    #     getMultiplier(nutrition_num, nutrition_unit, ingredient_num, ingredient_unit)

            




id = '52772'
ingredient = "chicken_breast"
names, links, images, ids  = searchRecipe(ingredient)
ingredients, name = getIngredients(ids[6], names[6])
print(getRecipeNutrition(ingredients, names[6]))