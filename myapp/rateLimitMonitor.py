# API can be called 5000 times a day
# Use Greptile to analyze your codebase and identify API calls that need rate limiting.
# Create a function that manages API calls and incorporates rate limiting logic.
# Use Greptile's natural language querying capabilities to dynamically fetch information about rate limits or API usage patterns from your codebase or documentation.
import os
import time
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get API keys from environment variables
greptile_api_key = os.getenv('greptile_api_key')
github_token = os.getenv('PAT')

# Global variable to keep track of API calls
api_call_count = 0

def query_greptile(query):
    repository_identifier = "github:main:cruedy/smart-recipe-book"
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
    global api_call_count
    
    # Query Greptile for rate limit info
    rate_limit_info = query_greptile("What's the rate limit for the Fat Secret API?")
    api_call_count_info = query_greptile("How many times is the Fat Secret API called in this codebase?")

    if rate_limit_info is None or api_call_count_info is None:
        print("Warning: Unable to get rate limit information from Greptile. Using default values.")
        rate_limit = 5000  # Default value
        api_call_count = 0  # Default value
    else:
        rate_limit = parse_rate_limit(rate_limit_info)
        api_call_count = parse_api_call_count(api_call_count_info)
    
    # Parse the rate limit info and API call count
    # (You'd need to implement the parsing logic based on Greptile's response)
    rate_limit = parse_rate_limit(rate_limit_info)
    api_call_count = parse_api_call_count(api_call_count_info)
    
    # Check if we're approaching the rate limit
    if api_call_count >= rate_limit * 0.9:  # 90% of the limit
        print("Warning: Approaching API rate limit. Waiting before next call.")
        time.sleep(60)  # Wait for 1 minute before the next call
    
    # Apply rate limiting
    time.sleep(1 / (rate_limit / 86400))  # Distribute calls evenly over a day
    
    # Make the actual API call
    api_call_count += 1
    return api_function(*args, **kwargs)

def parse_rate_limit(rate_limit_info):
    # Implement parsing logic based on Greptile's response
    # For now, we'll use a default value
    return 5000  # Default to 5000 calls per day

def parse_api_call_count(api_call_count_info):
    # Implement parsing logic based on Greptile's response
    # For now, we'll use the global variable
    global api_call_count
    return api_call_count

# Example usage
def fat_secret_api_call():
    # Simulate an API call
    print("Making Fat Secret API call")
    return "API response"

# Test the rate-limited function
for _ in range(10):
    result = rate_limited_api_call(fat_secret_api_call)
    print(f"API call result: {result}")
    print(f"Current API call count: {api_call_count}")