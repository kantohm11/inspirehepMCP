import requests

INSPIREHEP_API_URL = "https://inspirehep.net/api/literature"

def search_inspirehep(query):
    try:
        # Construct the API request URL
        url = f"{INSPIREHEP_API_URL}?q={query}"

        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        results = response.json()
        return results

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}