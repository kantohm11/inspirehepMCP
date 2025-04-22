import requests
from typing import Optional

INSPIREHEP_API_URL = "https://inspirehep.net/api/literature"

def search_inspirehep(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None
):
    try:
        # Remove surrounding quotes if present
        if query.startswith('"') and query.endswith('"'):
            query = query[1:-1]
        
        # Build parameters dictionary
        params = {'q': query}
        
        # Add optional parameters if provided
        if sort:
            params['sort'] = sort
        
        if page:
            params['page'] = page
        
        if size:
            # Ensure size is within the API limit (max 1000)
            size = min(size, 1000)
            params['size'] = size
        
        # Make the API request with params - requests library handles URL encoding properly
        response = requests.get(INSPIREHEP_API_URL, params=params)
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