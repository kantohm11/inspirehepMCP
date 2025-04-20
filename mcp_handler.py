import json
from inspirehep_client import search_inspirehep
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("InspireHEP")

@mcp.tool()
async def search(query: str, ctx: Context) -> str:
    """Search InspireHEP for a query."""
    results = search_inspirehep(query)
    return json.dumps(results)

async def process_mcp_request(request: str) -> str:
    try:
        data = json.loads(request)
        tool_name = data["tool_name"]
        arguments = data["arguments"]
        result = await mcp.call_tool(tool_name, arguments)
        if hasattr(result, "text"):
            return result.text
        return str(result)
    except Exception as e:
        return json.dumps({"error": str(e)})