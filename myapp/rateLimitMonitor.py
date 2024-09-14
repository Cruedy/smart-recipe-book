# API can be called 5000 times a day
# Use Greptile to analyze your codebase and identify API calls that need rate limiting.
# Create a function that manages API calls and incorporates rate limiting logic.
# Use Greptile's natural language querying capabilities to dynamically fetch information about rate limits or API usage patterns from your codebase or documentation.
import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import re

API_CALL_FILE = 'api_call_count.json'

def load_api_call_data():
    if os.path.exists(API_CALL_FILE):
        with open(API_CALL_FILE, 'r') as f:
            data = json.load(f)
        return data
    return []

def save_api_call_data(data):
    with open(API_CALL_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def clean_old_timestamps(data):
    current_time = datetime.now()
    return [timestamp for timestamp in data if current_time - datetime.fromisoformat(timestamp) < timedelta(days=1)]

def add_api_call():
    data = load_api_call_data()
    data = clean_old_timestamps(data)
    
    current_time = datetime.now().isoformat()
    data.append(current_time)
    
    save_api_call_data(data)
    return len(data)

def get_api_call_count():
    data = load_api_call_data()
    data = clean_old_timestamps(data)
    save_api_call_data(data)
    return len(data)

# Example usage
# def fat_secret_api_call():
#     # Simulate an API call
#     print("Making Fat Secret API call")
#     return "API response"

# # Test the rate-limited function
# for _ in range(10):
#     result = rate_limited_api_call(fat_secret_api_call)
#     print(f"API call result: {result}")

# Load environment variables
load_dotenv()

# Get API keys from environment variables
greptile_api_key = os.getenv('greptile_api_key')
github_token = os.getenv('PAT')

def query_greptile(query):
    # repository_identifier = "github:main:cruedy/smart-recipe-book"
    url = "https://api.greptile.com/v2/query"
    
    headers = {
        'Authorization': f'Bearer {greptile_api_key}',
        'X-Github-Token': github_token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "messages": [
            {
                "id": "query-1",
                "content": query,
                "role": "user"
            }
        ],
        "repositories": [
            {
                "remote": "github",
                "repository": "cruedy/smart-recipe-book",
                "branch": "main"
            }
        ],
        "sessionId": "rate-limit-session"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        if not response.text:
            print("Error: Empty response from Greptile API")
            return None
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Greptile API: {e}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        return None

def rate_limited_api_call(api_function, *args, **kwargs):
    rate_limit = 5000 # Assuming this is still the daily limit
    api_call_count = get_api_call_count()
    next_api_call = ''
    
    # Query Greptile for rate limit info
    rate_limit_info = query_greptile("What's the rate limit for the Fat Secret API?")
    next_api_call_info =  query_greptile("Base on the timestamps in api_call_count.json what time is 24 hours after the first time?")

    print("rate limit info: ", rate_limit_info)
    print("function api call: ", next_api_call_info)

    if rate_limit_info is None or next_api_call_info is None:
        print("Warning: Unable to get rate limit information from Greptile. Using default values.")
        rate_limit = 5000  # Default value
        next_api_call = ''  # Default value
    else:
        print("here")
        print("here")
        rate_limit = parse_rate_limit(rate_limit_info)
        fat_secret_api_call = parse_api_call_count(next_api_call_info)
        print("rate_limit: ", rate_limit)
    
    if api_call_count >= rate_limit:
        print("Error: API call limit reached. Please try again later.")
        return None
    
    # Check if we're approaching the rate limit
    if api_call_count >= rate_limit * 0.9:  # 90% of the limit
        print("Warning: Approaching API rate limit. Waiting before next call.")
        time.sleep(15)  # Wait for 15 sec before the next call
    
    # Apply rate limiting
    # time.sleep(1 / (rate_limit / 86400))  # Distribute calls evenly over a day
    
    # Make the actual API call
    new_count = add_api_call()
    print(f"API call made. Current count: {new_count}")
    return api_function(*args, **kwargs)

def parse_rate_limit(rate_limit_info):
    if rate_limit_info and 'message' in rate_limit_info:
        message = rate_limit_info['message']
        # Look for the rate limit value in the message
        match = re.search(r'rate limit (?:of|is) ([\d,]+)', message, re.IGNORECASE)
        if match:
            return int(match.group(1).replace(',', ''))
    # If parsing fails, return the default value
    return None

def parse_api_call_count(api_call_count_info):
    if api_call_count_info and 'message' in api_call_count_info:
        message = api_call_count_info['message']
        
        # Use regex to find function names associated with Fat Secret API
        pattern = r'(\w+\([^)]*\))\s+.*?Fat Secret API'
        matches = re.findall(pattern, message)
        
        if matches:
            print(f"Found functions using Fat Secret API: {matches}")
            return matches
        else:
            print("No functions found that directly use the Fat Secret API.")
    
    return []

# Example usage
def fat_secret_api_call():
    # Simulate an API call
    print("Making Fat Secret API call")
    return "API response"

# # Test the rate-limited function
for _ in range(10):
    result = rate_limited_api_call(fat_secret_api_call)
    print(f"API call result: {result}")
    call_count = add_api_call()
    print(f"Current API call count: {call_count}")