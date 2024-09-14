import http.client
import urllib.parse
import time
import hmac
import hashlib
import base64
import uuid
import json 
import re
from dotenv import load_dotenv
import os
from rateLimitMonitor import rate_limited_api_call

# Helper functions
def generate_nonce():
    return str(uuid.uuid4().hex)

def generate_timestamp():
    return str(int(time.time()))

def percent_encode(string):
    return urllib.parse.quote(string, safe='')

def generate_signature_base_string(http_method, base_url, params):
    sorted_params = '&'.join(['{}={}'.format(percent_encode(k), percent_encode(v)) for k, v in sorted(params.items())])
    return '&'.join([http_method.upper(), percent_encode(base_url), percent_encode(sorted_params)])

def generate_signature(signature_base_string, consumer_secret, token_secret=''):
    signing_key = '&'.join([percent_encode(consumer_secret), percent_encode(token_secret)])
    hashed = hmac.new(signing_key.encode('utf-8'), signature_base_string.encode('utf-8'), hashlib.sha1)
    return base64.b64encode(hashed.digest()).decode('utf-8')

def searchIngredient(ingredient):
    load_dotenv()
    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')

    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': generate_timestamp(),
        'oauth_nonce': generate_nonce(),
        'oauth_version': '1.0',
    }

    api_params = {
        'method': 'foods.search',
        'search_expression': ingredient,
        'format': 'json',
        'max_results': '10',
        'page_number': '0'
    }

    all_params = {**oauth_params, **api_params}

    base_url = 'https://platform.fatsecret.com/rest/server.api'
    signature_base_string = generate_signature_base_string('GET', base_url, all_params)

    oauth_signature = generate_signature(signature_base_string, consumer_secret)
    all_params['oauth_signature'] = oauth_signature

    def make_get_request(base_url, all_params, retries=3, delay=2):
        for attempt in range(retries):
            try:
                conn = http.client.HTTPSConnection('platform.fatsecret.com')
                query_string = urllib.parse.urlencode(all_params)
                conn.request('GET', f'/rest/server.api?{query_string}')
                response = conn.getresponse()
                data = response.read().decode('utf-8')
                conn.close()
                return data
            except Exception as e:
                print(f"Exception occurred: {e}. Retrying...")
            # Wait before retrying the request
            time.sleep(delay)
        print("Max retries exceeded. Returning None.")
        return None  # Return None if max retries are exceeded

    response = rate_limited_api_call(make_get_request, base_url, all_params)
    # response = make_get_request(base_url, all_params)
    
    # Parse the JSON response into a dictionary
    response_dict = json.loads(response)
    
    # Access the "food_description" for each food item
    foods = response_dict.get('foods', {}).get('food', [])

    # using regular experession to change format of food description to dictionary
    pattern = r"Per (?P<amount>[\d\s\w]+) - Calories: (?P<calories>\d+kcal) \| Fat: (?P<fat>\d+\.\d+g) \| Carbs: (?P<carbs>\d+\.\d+g) \| Protein: (?P<protein>\d+\.\d+g)"

    food_description = ""
    # print("foods_type:", type(foods))
    # print("foods:", foods)
    if foods == [] or foods == {}:
        # print(f"No results found for ingredient: {ingredient}")
        return None
    if type(foods) == dict:
        food_description = foods['food_description']
    else:
        food_description = foods[0].get('food_description', None)
    
    # if foods
    if food_description == None:
        # print(f"Food description is None for ingredient: {ingredient}")
        return None
    # print("foods_description:", food_description)
    match = re.search(pattern, food_description)

    # print("match: ", match)
    if match == None:
        # print(f"Regex pattern did not match for ingredient: {ingredient}. Description: {food_description}")
        return None

    nutrition = match.groupdict()
    

    results = {}
    results[ingredient] = nutrition
    # print("results", results)
    return results

# Test the function
# print(searchIngredient("1 cup Toor dal"))

# ['1 lb Salmon', '1 tablespoon Olive oil', '2 tablespoons Soy Sauce', '2 tablespoons Sake', '4 tablespoons Sesame Seed']
