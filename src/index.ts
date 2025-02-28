#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  McpError,
  ErrorCode,
} from '@modelcontextprotocol/sdk/types.js';

class MinimalMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'minimal-mcp-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();

    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'echo_tool',
          description: 'Echoes back the input string',
          inputSchema: {
            type: 'object',
            properties: {
              message: {
                type: 'string',
                description: 'The message to echo back',
              },
            },
            required: ['message'],
          },
        },
      ],
    }));

    // Handle the echo_tool
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name !== 'echo_tool') {
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${request.params.name}`
        );
      }

      const args = request.params.arguments as { message: string };
      const { message } = args;
      if (typeof message !== 'string') {
        throw new McpError(
          ErrorCode.InvalidParams,
          'Invalid input: "message" must be a string'
        );
      }

      return {
        content: [
          {
            type: 'text',
            text: `Echo: ${message}`,
          },
        ],
      };
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Minimal MCP server running on stdio');
  }
}

const server = new MinimalMCPServer();
server.run().catch(console.error);
