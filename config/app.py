from fastapi import FastAPI
from config.lifespan import combine_lifespans
from main import mcp_server

# --- Initialize FastAPI and FastMCP ---
mcp_stream_app = mcp_server.http_app(
    path="/",
    transport="streamable-http",
)

fastapi_app = FastAPI(
    title="Star Wars HoloNet MCP Server",
    description="A FastMCP server providing tools to access the Star Wars API (SWAPI).",
    lifespan=combine_lifespans(mcp_stream_app.router.lifespan_context),
)

# Mount the MCP server to your FastAPI app at the /mcp endpoint
fastapi_app.mount(
    "/mcp",
    mcp_stream_app,
)
