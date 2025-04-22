# MCP Server Plan

This document outlines the detailed plan for creating a Python-based MCP server that communicates via standard input/output (stdio). The server is designed to fetch search queries from Inspirehep and is implemented as a CLI tool.

## 1. Setup and Environment

- **Python Version:** 3.9 or later.
- **Dependencies:**
  - The MCP Protocol Python SDK from [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk).
  - Standard Python libraries (e.g., `sys` for stdio operations).
  - [Requests](https://docs.python-requests.org/) for making HTTP calls.

## 2. Project Structure

The project is structured as a simple CLI tool:
- **server.py:** Main entry point. Reads MCP messages from stdio, processes requests, and writes responses to stdio.
- **mcp_handler.py:** Contains logic for parsing MCP messages and formatting responses using the MCP SDK.
- **inspirehep_client.py:** Implements functions to call the Inspirehep search API based on the specifications in [inspirehep/rest-api-doc](https://github.com/inspirehep/rest-api-doc).
- **requirements.txt (optional):** Lists required packages.

## 3. Implementation Steps

1. **Reading from Standard Input:**
   - Continuously read incoming MCP messages using `sys.stdin`.
   - Parse and validate each message using the MCP SDK.

2. **Handling MCP Requests:**
   - Extract the search query from the MCP message.
   - Validate and log the query as necessary.

3. **Fetching Data from Inspirehep:**
   - Use the extracted query to construct an HTTP request to the Inspirehep API.
   - Retrieve and process search results based on the endpoint and parameters specified in the Inspirehep REST API documentation.

4. **Returning the Response:**
   - Format the API result to comply with the MCP protocol.
   - Write the formatted response back to standard output.

5. **Error Handling & Logging:**
   - Include robust error handling for MCP message parsing and API calls.
   - Return valid MCP error messages through stdio if needed.

## 4. Deployment & Execution

- **Local Execution:** Run the server using: `python server.py`
- **Testing:** Simulate MCP messages by piping input via scripts or using `echo` with redirection.
- **Logging:** Implement logging to monitor request handling and errors.

## 5. Mermaid Diagram

```mermaid
sequenceDiagram
    participant User as MCP Client (via stdio)
    participant Server as Python MCP Server (server.py)
    participant Handler as MCP Handler (mcp_handler.py)
    participant Inspirehep as Inspirehep API
    User->>Server: Write MCP Search Query via stdio
    Server->>Handler: Parse and validate MCP message
    Handler->>Inspirehep: Send search query request
    Inspirehep-->>Handler: Return API search results
    Handler-->>Server: Format response into MCP format
    Server-->>User: Write MCP response via stdio