import json
from inspirehep_client import search_inspirehep
from mcp.server.fastmcp import FastMCP
from typing import Optional

# Create the MCP server instance
mcp = FastMCP("InspireHEP")

@mcp.tool()
def search(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None
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
             - "tc conference paper" (only conference papers)
             - "doi:10.1103/PhysRevLett.19.1264" (paper with a specific DOI)
    
    - sort: Sort order for results. Options:
            - "mostrecent" (default when no query is provided)
            - "mostcited" (records with most citations appear first)
    
    - page: Page number for pagination (default: 1)
    
    - size: Number of results per page (default: 10, max: 1000)
    """
    # Call the InspireHEP API through our client
    results = search_inspirehep(query, sort=sort, page=page, size=size)
    
    # Return the results directly as a dictionary
    # FastMCP will handle the serialization
    return results