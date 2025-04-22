import subprocess
import sys
import json

def test_manual_query():
    """Test the InspireHEP MCP server by directly sending a query through stdin."""
    print("Testing InspireHEP MCP server with direct query...")
    
    # Create a query based on the query.json example
    query = {
        "tool_name": "search",
        "arguments": {"query": "higgs boson"}
    }
    
    # Start the server process
    server_process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Convert the query to JSON and send it
        query_json = json.dumps(query)
        print(f"Sending query: {query_json}")
        
        server_process.stdin.write(query_json + "\n")
        server_process.stdin.flush()
        
        # Read the response with a timeout
        stdout, stderr = server_process.communicate(timeout=10)
        
        # Check for errors
        if stderr:
            print(f"Error from server: {stderr}")
        
        # Process the response
        if stdout:
            try:
                print("Received response from server")
                # Try to parse as JSON for pretty printing
                response = json.loads(stdout)
                print(json.dumps(response, indent=2)[:1000] + "..." if len(json.dumps(response, indent=2)) > 1000 else "")
                print("\nServer test completed successfully!")
                return 0
            except json.JSONDecodeError:
                print(f"Failed to parse response as JSON: {stdout[:200]}...")
                return 1
        else:
            print("No response received from server")
            return 1
    
    except subprocess.TimeoutExpired:
        print("Server process timed out after 10 seconds")
        server_process.kill()
        return 1
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return 1
    finally:
        # Ensure the server process is terminated
        if server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == "__main__":
    # Use a simpler test approach
    exit_code = test_manual_query()
    sys.exit(exit_code)