# API can be called 5000 times a day
# Use Greptile to analyze your codebase and identify API calls that need rate limiting.
# Create a function that manages API calls and incorporates rate limiting logic.
# Use Greptile's natural language querying capabilities to dynamically fetch information about rate limits or API usage patterns from your codebase or documentation.
import time
from greptile import Greptile
from dotenv import load_dotenv
import os



def rate_limited_api_call(api_function, *args, **kwargs):
    load_dotenv()
    api_key= os.getenv('greptile_api_key')
    greptile = Greptile(api_key=api_key)
    
    # Query Greptile for rate limit info
    rate_limit_info = greptile.query("What's the rate limit for this API call?")
    
    # Parse the rate limit info and apply it
    # (You'd need to implement the parsing logic based on Greptile's response)
    rate_limit = parse_rate_limit(rate_limit_info)
    
    # Apply rate limiting
    time.sleep(1 / rate_limit)
    
    # Make the actual API call
    return api_function(*args, **kwargs)