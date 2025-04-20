import sys
import json
import asyncio
from mcp_handler import process_mcp_request, mcp

async def main():
    while True:
        # Read input from stdin
        line = sys.stdin.readline().strip()

        if not line:
            break  # Exit loop if stdin is closed

        try:
            # Process the input line
            response = await process_mcp_request(line)

            # Write the response to stdout
            sys.stdout.write(response + "\\n")
            sys.stdout.flush()
        except Exception as e:
            error_message = json.dumps({"error": str(e)})
            sys.stdout.write(error_message + "\\n")
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
