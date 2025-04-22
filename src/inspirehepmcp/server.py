import asyncio
import sys
import json
from .mcp_handler import mcp

def main():
    """Run the InspireHEP MCP server."""
    # Using the run method to properly start the FastMCP server
    # with full MCP protocol support
    mcp.run()

if __name__ == "__main__":
    main()
