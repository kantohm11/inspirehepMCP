import requests
from typing import Optional, Dict, List, Any

INSPIREHEP_API_URL = "https://inspirehep.net/api/literature"

def search_inspirehep(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None,
    include_abstract: bool = False
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
        
        # Always filter the results, with abstract optional
        results = filter_response(results, include_abstract)
        
        # Return the results
        return results
    
    except requests.exceptions.RequestException as e:
        # Return a structured error response
        return {
            "error": True,
            "message": f"Error fetching data from InspireHEP: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }

def filter_response(response: Dict[str, Any], include_abstract: bool = False) -> Dict[str, Any]:
    """
    Filter the InspireHEP API response to include only essential information.
    
    Args:
        response: The full response from InspireHEP API
        include_abstract: Whether to include the abstract in the results
        
    Returns:
        A filtered response containing only essential information
    """
    if "error" in response:
        # Return error responses unfiltered
        return response
    
    filtered_response = {
        "hits": {
            "total": response["hits"]["total"] if "total" in response["hits"] else 0,
            "hits": []
        }
    }
    
    # Keep pagination links if they exist
    if "links" in response and "next" in response["links"]:
        filtered_response["links"] = {
            "next": response["links"]["next"]
        }
    
    # Process each hit/record
    for hit in response["hits"]["hits"]:
        filtered_hit = {
            "id": hit.get("control_number", hit.get("id", "")),
            "title": _extract_title(hit),
            "authors": _extract_authors(hit),
            "publication_info": _extract_publication_info(hit),
            "citation_count": _extract_citation_count(hit),
        }
        
        # Include abstract only if requested
        if include_abstract:
            filtered_hit["abstract"] = _extract_abstract(hit)
        
        # Add preprint information if available
        preprint_info = _extract_preprint_info(hit)
        if preprint_info:
            filtered_hit["preprint_info"] = preprint_info
        
        # Add DOI if available
        doi = _extract_doi(hit)
        if doi:
            filtered_hit["doi"] = doi
        
        filtered_response["hits"]["hits"].append(filtered_hit)
    
    return filtered_response

def _extract_title(hit: Dict[str, Any]) -> str:
    """Extract the primary title from a hit."""
    if "metadata" in hit and "titles" in hit["metadata"] and hit["metadata"]["titles"]:
        return hit["metadata"]["titles"][0].get("title", "")
    return ""

def _extract_authors(hit: Dict[str, Any]) -> List[str]:
    """Extract a simplified list of author names."""
    authors = []
    if "metadata" in hit and "authors" in hit["metadata"]:
        for author in hit["metadata"]["authors"]:
            if "full_name" in author:
                authors.append(author["full_name"])
    return authors

def _extract_abstract(hit: Dict[str, Any]) -> str:
    """Extract the primary abstract text."""
    if "metadata" in hit and "abstracts" in hit["metadata"] and hit["metadata"]["abstracts"]:
        return hit["metadata"]["abstracts"][0].get("value", "")
    return ""

def _extract_publication_info(hit: Dict[str, Any]) -> Dict[str, Any]:
    """Extract publication information."""
    pub_info = {}
    if "metadata" in hit and "publication_info" in hit["metadata"] and hit["metadata"]["publication_info"]:
        info = hit["metadata"]["publication_info"][0]
        if "journal_title" in info:
            pub_info["journal"] = info["journal_title"]
        if "journal_volume" in info:
            pub_info["volume"] = info["journal_volume"]
        if "year" in info:
            pub_info["year"] = info["year"]
        if "page_start" in info:
            pub_info["page"] = info["page_start"]
    return pub_info

def _extract_citation_count(hit: Dict[str, Any]) -> int:
    """Extract the citation count."""
    if "metadata" in hit and "citation_count" in hit["metadata"]:
        return hit["metadata"]["citation_count"]
    return 0

def _extract_doi(hit: Dict[str, Any]) -> str:
    """Extract the primary DOI."""
    if "metadata" in hit and "dois" in hit["metadata"] and hit["metadata"]["dois"]:
        return hit["metadata"]["dois"][0].get("value", "")
    return ""

def _extract_preprint_info(hit: Dict[str, Any]) -> Dict[str, Any]:
    """Extract preprint information including arXiv ID and categories."""
    preprint_info = {}
    
    if "metadata" not in hit:
        return preprint_info
    
    # Extract preprint date if available
    if "preprint_date" in hit["metadata"]:
        preprint_info["date"] = hit["metadata"]["preprint_date"]
    
    # Extract arXiv information if available
    if "arxiv_eprints" in hit["metadata"] and hit["metadata"]["arxiv_eprints"]:
        arxiv_data = hit["metadata"]["arxiv_eprints"][0]
        if "value" in arxiv_data:
            preprint_info["arxiv_id"] = arxiv_data["value"]
            
        if "categories" in arxiv_data:
            preprint_info["arxiv_categories"] = arxiv_data["categories"]
            
    # If we have links section, check for arXiv link there too
    if "links" in hit and isinstance(hit["links"], dict):
        for link_key, link_url in hit["links"].items():
            if "arxiv" in link_key.lower() and isinstance(link_url, str):
                preprint_info["arxiv_url"] = link_url
                break
    
    # If we have an arxiv_id but no URL was found, use a fallback URL pattern
    # This is only used if we couldn't find the URL in the raw data
    if "arxiv_id" in preprint_info and "arxiv_url" not in preprint_info:
        preprint_info["arxiv_url"] = f"https://arxiv.org/abs/{preprint_info['arxiv_id']}"
    
    return preprint_info