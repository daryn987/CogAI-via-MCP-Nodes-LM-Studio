#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { setupTools } from './tools/setupTools.js';
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import express from 'express';
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import { randomUUID } from "node:crypto";
import cors from 'cors';
import { config } from "./config.js";
async function main() {
    // Create MCP server
    const server = new McpServer({
        name: 'web-search',
        version: '1.2.0'
    });
    // Set up server tools
    setupTools(server);
    // Enable STDIO mode if MODE is 'both' or 'stdio' or not specified
    if (process.env.MODE === undefined || process.env.MODE === 'both' || process.env.MODE === 'stdio') {
        console.error('🔌 Starting STDIO transport...');
        const stdioTransport = new StdioServerTransport();
        await server.connect(stdioTransport).then(() => {
            console.error('✅ STDIO transport enabled');
        }).catch(error => {
            console.error('❌ Failed to initialize STDIO transport:', error);
        });
    }
    // Only set up HTTP server if enabled
    if (config.enableHttpServer) {
        console.error('🔌 Starting HTTP server...');
        // 创建 Express 应用
        const app = express();
        app.use(express.json());
        // 是否启用跨域
        if (config.enableCors) {
            app.use(cors({
                origin: config.corsOrigin || '*',
                methods: ['GET', 'POST', 'DELETE'],
            }));
            app.options('*', cors());
        }
        // Store transports for each session type
        const transports = {
            streamable: {},
            sse: {}
        };
        // Handle POST requests for client-to-server communication
        app.post('/mcp', async (req, res) => {
            // Check for existing session ID
            const sessionId = req.headers['mcp-session-id'];
            let transport;
            if (sessionId && transports.streamable[sessionId]) {
                // Reuse existing transport
                transport = transports.streamable[sessionId];
            }
            else if (!sessionId && isInitializeRequest(req.body)) {
                // New initialization request
                transport = new StreamableHTTPServerTransport({
                    sessionIdGenerator: () => randomUUID(),
                    onsessioninitialized: (sessionId) => {
                        // Store the transport by session ID
                        transports.streamable[sessionId] = transport;
                    },
                    // DNS rebinding protection is disabled by default for backwards compatibility. If you are running this server
                    // locally, make sure to set:
                    // enableDnsRebindingProtection: true,
                    // allowedHosts: ['127.0.0.1'],
                });
                // Clean up transport when closed
                transport.onclose = () => {
                    if (transport.sessionId) {
                        delete transports.streamable[transport.sessionId];
                    }
                };
                // Connect to the MCP server
                await server.connect(transport);
            }
            else {
                // Invalid request
                res.status(400).json({
                    jsonrpc: '2.0',
                    error: {
                        code: -32000,
                        message: 'Bad Request: No valid session ID provided',
                    },
                    id: null,
                });
                return;
            }
            // Handle the request
            await transport.handleRequest(req, res, req.body);
        });
        // Reusable handler for GET and DELETE requests
        const handleSessionRequest = async (req, res) => {
            const sessionId = req.headers['mcp-session-id'];
            if (!sessionId || !transports.streamable[sessionId]) {
                res.status(400).send('Invalid or missing session ID');
                return;
            }
            const transport = transports.streamable[sessionId];
            await transport.handleRequest(req, res);
        };
        // Handle GET requests for server-to-client notifications via SSE
        app.get('/mcp', handleSessionRequest);
        // Handle DELETE requests for session termination
        app.delete('/mcp', handleSessionRequest);
        // Legacy SSE endpoint for older clients
        app.get('/sse', async (req, res) => {
            // Create SSE transport for legacy clients
            const transport = new SSEServerTransport('/messages', res);
            transports.sse[transport.sessionId] = transport;
            res.on("close", () => {
                delete transports.sse[transport.sessionId];
            });
            await server.connect(transport);
        });
        // Legacy message endpoint for older clients
        app.post('/messages', async (req, res) => {
            const sessionId = req.query.sessionId;
            const transport = transports.sse[sessionId];
            if (transport) {
                await transport.handlePostMessage(req, res, req.body);
            }
            else {
                res.status(400).send('No transport found for sessionId');
            }
        });
        // Read the port number from the environment variable; use the default port 3000 if it is not set.
        const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
        app.listen(PORT, '0.0.0.0', () => {
            console.error(`✅ HTTP server running on port ${PORT}`);
        });
    }
    else {
        console.error('ℹ️ HTTP server disabled, running in STDIO mode only');
    }
}
main().catch(console.error);
