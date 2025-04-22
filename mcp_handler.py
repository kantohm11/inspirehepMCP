import json
from inspirehep_client import search_inspirehep, get_bibtex, open_arxiv_in_browser
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
    - query: Search query string. For literature records, a custom search syntax is used.
             Examples:
             - "a Edward.Witten.1" (papers by author Edward Witten)
             - "t boson" (papers with "boson" in the title)
             - "topcite 1000+" (papers cited at least 1000 times)
             - "doi:10.1103/PhysRevLett.19.1264" (paper with a specific DOI)
             - "refersto:recid:2901053" (papers that reference a specific record, specified by inspireHEP record identifier)
    
    - sort: Sort order for results. Options:
            - "mostrecent" (default when no query is provided)
            - "mostcited" (records with most citations appear first)
    
    - page: Page number for pagination (default: 1)
    
    - size: Number of results per page (default: 10, max: 1000)
    
    - include_abstract: If True, includes the abstract text in the results.
                        Default: False (omits abstracts for more concise results)
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

@mcp.tool()
def open_arxiv_in_browser(url: str) -> dict:
    """
    Opens an arXiv URL in the user's default web browser.
    
    Parameters:
    - url: The arXiv URL to open. Must start with http:// or https:// and must be from arxiv.org
          Example: "https://arxiv.org/abs/2104.08394"
    
    Returns a dictionary with the result of the operation.
    This tool allows users to quickly view arXiv preprints directly in their browser.
    Only URLs from arxiv.org domain are allowed for security reasons.
    """
    # Call the client function to open the arXiv URL in browser
    result = open_arxiv_in_browser(url)
    
    # Return the result
    return result