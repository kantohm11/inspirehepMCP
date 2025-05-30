import json
from .inspirehep_client import search_inspirehep, get_bibtex
from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any

# Create the MCP server instance
mcp = FastMCP("InspireHEP")

@mcp.tool()
def search(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None,
    include_abstract: bool = False
) -> dict:
    """
    Search InspireHEP for articles matching the query.
    Returns research papers from the high energy physics literature database.
    
    Parameters:
    - query: Search query string. For literature records, a custom search syntax is used. If you fail to find what you are looking for, try using the google-like search syntax. The complete syntax is available at "https://help.inspirehep.net/knowledge-base/inspire-paper-search/" .
             Examples:
             - "a Edward.Witten.1" (papers by author Edward Witten)
             - "t boson" (papers with "boson" in the title)
             - "topcite 1000+" (papers cited at least 1000 times)
             - "doi:10.1103/PhysRevLett.19.1264" (paper with a specific DOI)
             - "refersto:recid:2901053" (papers that reference a specific record, specified by inspireHEP record identifier)
             - "gaiotto duality" (google-like search loosely matching title, abstract, and author names)
    
    - sort: Sort order for results. Options:
            - "mostrecent" (default)
            - "mostcited" (records with most citations appear first)
    
    - page: Page number for pagination (default: 1)
    
    - size: Number of results per page (default: 10, max: 1000)
    
    - include_abstract: If True, includes the abstract text in the results. (default: False)
    """
    # Call the InspireHEP API through our client
    results = search_inspirehep(query, sort=sort, page=page, size=size, include_abstract=include_abstract)
    
    # Return the results directly as a dictionary
    # FastMCP will handle the serialization
    return results

@mcp.tool()
def get_bibtex_citation(record_id: str) -> dict:
    """
    Fetch BibTeX citation for an InspireHEP record by its ID.
    
    Parameters:
    - record_id: The InspireHEP record ID (control number)
                Example: "451647" for a specific paper
    
    Returns a dictionary containing the record ID and BibTeX citation string.
    This can be used directly in LaTeX documents or reference management software.
    """
    # Call the InspireHEP API through our client to get the BibTeX
    result = get_bibtex(record_id)
    
    # Return the result (either the BibTeX or an error message)
    # FastMCP will handle the serialization
    return result