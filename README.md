# InspireHEP MCP

A Model Context Protocol (MCP) server for interacting with the [InspireHEP](https://inspirehep.net/) database of high-energy physics research papers.

## Description

InspireHEP MCP provides an API for searching, retrieving, and interacting with high-energy physics research papers from the InspireHEP database. This project implements the Model Context Protocol (MCP) to allow AI assistants and other tools to query the InspireHEP database in a structured way.

## Features

- **Search InspireHEP**: Perform advanced searches for research papers with custom query syntax
- **Get BibTeX Citations**: Retrieve BibTeX citations for specific papers
- **MCP Integration**: Full integration with MCP for AI tool use

## Installation


## Usage

### Running from github repo

E.g. with uv:
```bash
uvx --from git+https://github.com/kantohm11/inspirehepMCP inspirehepmcp
```

### Running in Docker

Pull a docker image to work with if you don't have. 
E.g. with uv:
```bash
docker pull ghcr.io/astral-sh/uv:0.7.8-python3.13-bookworm
```
and then run the server:
```bash
docker run --rm -i ghcr.io/astral-sh/uv:0.7.8-python3.13-bookworm uvx --from git+https://github.com/kantohm11/inspirehepMCP inspirehepmcp
```

### Using the MCP Inspector

You can use the MCP Inspector to test and debug your InspireHEP MCP server implementation:

```bash
# Run the MCP Inspector to inspect and test your MCP server running in Docker
npx @modelcontextprotocol/inspector docker run --rm -i ghcr.io/astral-sh/uv:0.7.8-python3.13-bookworm uvx --from git+https://github.com/kantohm11/inspirehepMCP inspirehepmcp
```
or the server running locally
```bash
# Run the MCP Inspector to inspect and test your MCP server running locally 
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/kantohm11/inspirehepMCP inspirehepmcp
```


The MCP Inspector provides a web interface to:
- Explore available tools
- Test tool invocations
- View request/response payloads
- Debug your MCP server implementation

### VS Code Integration with GitHub Copilot

To use InspireHEP MCP with GitHub Copilot in VS Code, add the following configuration to your VS Code `settings.json` file:

```json
"mcp": {
    "servers": [
    {
        "name": "InspireHEP",
        "type": "stdio",
        "command": "uvx",
        "args": ["--from", "git+https://github.com/kantohm11/inspirehepMCP", "inspirehepmcp"],
        "enabled": true
    }
  ]
}
```


With this configuration, GitHub Copilot will be able to access InspireHEP data through the MCP server, allowing you to search for physics papers, get citations, and more directly from within VS Code.

### Available Tools

The MCP server exposes the following tools:

#### search

Search InspireHEP for articles matching a query string.

```python
search(
    query: str, 
    sort: Optional[str] = None, 
    page: Optional[int] = None, 
    size: Optional[int] = None,
    include_abstract: bool = False
)
```

**Parameters:**
- `query`: Search query string. Examples:
  - `"a Edward.Witten.1"` (papers by author Edward Witten)
  - `"t boson"` (papers with "boson" in the title)
  - `"topcite 1000+"` (papers cited at least 1000 times)
  - `"doi:10.1103/PhysRevLett.19.1264"` (paper with a specific DOI)
  - `"refersto:recid:2901053"` (papers that reference a specific record)
- `sort`: Sort order for results. Options:
  - `"mostrecent"` (default when no query is provided)
  - `"mostcited"` (records with most citations appear first)
- `page`: Page number for pagination (default: 1)
- `size`: Number of results per page (default: 10, max: 1000)
- `include_abstract`: If True, includes the abstract text in the results (default: False)

#### get_bibtex_citation

Fetch BibTeX citation for an InspireHEP record by its ID.

```python
get_bibtex_citation(record_id: str)
```

## Development

### Project Structure

```
inspirehepmcp/
├── src/inspirehepmcp/
│   ├── __init__.py
│   ├── inspirehep_client.py  # InspireHEP API client
│   ├── mcp_handler.py        # MCP tool definitions
│   └── server.py             # MCP server startup
├── doc/                      # Documentation
└── pyproject.toml            # Project configuration
```

### Dependencies

- `mcp[cli]>=1.6.0`: Model Context Protocol framework
- `requests>=2.32.3`: HTTP library for API requests

