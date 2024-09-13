# from flask import Flask
from recipeSearch import *
import functools
from concurrent.futures import ThreadPoolExecutor, as_completed

# app = Flask(__name__)

# @app.route('/api/route')
def getMacros():
    return "Prediction Route Working!" 

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

def fetch_and_nutrition(recipe):
    """
    Fetches ingredients and computes nutrition for a given recipe.
    :param recipe: A list representing a recipe, where recipe[3] is the idMeal.
    :return: A tuple (calories, fat, carbs, protein) if successful, None otherwise.
    """
    print("recipe: ", recipe)
    print("mealID: ", recipe[3])
    ingredients = getIngredients(recipe[3])  # r[3] is the idMeal
    if ingredients is not None:
        print("ingredients: ", ingredients)
        # print("nutrition: ", getRecipeNutrition(ingredients))
        return getRecipeNutrition(ingredients)
    return None
# recipe = ['Beef stroganoff', 'https://www.themealdb.com/meal/52834', 'https://www.themealdb.com/images/media/meals/svprys1511176755.jpg', '52834']
# print(fetch_and_nutrition(recipe))

# recipe = ['Bitterballen (Dutch meatballs)', 'https://www.themealdb.com/meal/52979', 'https://www.themealdb.com/images/media/meals/lhqev81565090111.jpg', '52979']
# print("result", fetch_and_nutrition(recipe))
  
def returnFoodList(minCalories, maxCalories, maxFat, maxCarbs, minProtein, ingredient):
    filtered_recipes = []
    nutritious_recipes = []
    
    # Get all recipes and filter based on nutrition
    print("gettting Recipes")
    recipes = getAllRecipes()
    print("Total recipes: ", len(recipes))
    
    for r in recipes:
        # print("recipe: ", r)
        ingredients = getIngredients(r[3])  # r[3] is the idMeal
        if ingredients is not None:
            calories, fat, carbs, protein = getRecipeNutrition(ingredients)
            print("nutrition: ", calories, fat, carbs, protein, r[0])
            if (minCalories == 0 or calories >= minCalories) and \
                (maxCalories == 0 or calories <= maxCalories) and \
                (maxFat == 0 or fat <= maxFat) and \
                (maxCarbs == 0 or carbs <= maxCarbs) and \
                (minProtein == 0 or protein >= minProtein):
                nutritious_recipes.append(r)
    
    # Get recipes that match the ingredient
    ingredient_recipes = fromIngredient(ingredient)
    print("length: ", len(ingredient_recipes))
    ingredient_ids = set(i[3] for i in ingredient_recipes)# Get just the ids
    
    # Filter nutritious recipes based on whether the idMeal is in the ingredient recipes
    for n in nutritious_recipes:
        if n[3] in ingredient_ids:
            # print("Matching recipe: ", n)
            filtered_recipes.append(n)
    
    return filtered_recipes

food_list = returnFoodList(0, 100, 0, 0, 0, 'beef')
print(food_list)
print("full length: ", len(food_list))

# threading for returnFoodList
# with ThreadPoolExecutor(max_workers=1) as executor:  # Adjust max_workers as needed
#         future_to_recipe = {executor.submit(fetch_and_nutrition, r): r for r in recipes}
        
#         for future in as_completed(future_to_recipe):
#             recipe = future_to_recipe[future]
#             try:
#                 # Get the fetched ingredients and calculated nutrition
#                 nutrition = future.result()
#                 if nutrition:
#                     calories, fat, carbs, protein = nutrition
#                     print("nutrition and recipe: ", nutrition, recipe)
#                     # Apply the same filter logic as in the original function
#                     if (minCalories == 0 or calories >= minCalories) and \
#                        (maxCalories == 0 or calories <= maxCalories) and \
#                        (maxFat == 0 or fat <= maxFat) and \
#                        (maxCarbs == 0 or carbs <= maxCarbs) and \
#                        (minProtein == 0 or protein >= minProtein):
#                         nutritious_recipes.append(recipe)
#             except Exception as exc:
#                 print(f"Error processing recipe {recipe[3]}: {exc}")