import requests
from urllib.parse import quote
from typing import Optional

INSPIREHEP_API_URL = "https://inspirehep.net/api/literature"

def search_inspirehep(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None
):
    try:
        # URL encode the query parameter to handle spaces and special characters
        encoded_query = quote(query)
        
        # Start building the API request URL
        url = f"{INSPIREHEP_API_URL}?q={encoded_query}"
        
        # Add optional parameters if provided
        if sort:
            url += f"&sort={sort}"
        
        if page:
            url += f"&page={page}"
        
        if size:
            # Ensure size is within the API limit (max 1000)
            size = min(size, 1000)
            url += f"&size={size}"
        
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        results = response.json()
        
        # Return the results
        return results
    
    except requests.exceptions.RequestException as e:
        # Return a structured error response
        return {
            "error": True,
            "message": f"Error fetching data from InspireHEP: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }