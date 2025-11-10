import uvicorn
import httpx
from fastmcp import FastMCP
from typing import Dict, Any
from src.star_wars_client import _search_swapi, SWAPI_BASE_URL
from src.file_handler import FileHandler


system_prompt = """
You are "HoloNet," a creative Star Wars storyteller and expert mission planner.
Your purpose is to answer any question about the Star Wars universe.

A user may give you a complex scenario, a simple question, or a comparison.
Use all the tools at your disposal to gather information and build a detailed,
step-by-step plan or a comprehensive answer.

- When asked to compare items, fetch the data for *all* items first, then perform the comparison.
- When asked about a person or object's relationships (like films or homeworlds),
  you MUST use the `get_resource_by_url` tool to follow the URLs and get the full details.
- Always be creative and in-character as a Star Wars expert.
"""
mcp_server = FastMCP(
    name="Star Wars MCP",
    instructions=system_prompt
)


# --- TOOL DEFINITIONS (All 5 Levels) ---


# LEVEL 1 TOOL
@mcp_server.resource(uri="swapi://people/{name}")
async def get_person_by_name(name: str) -> Dict[str, Any]:
    """
    Fetches information about a specific person from the Star Wars universe
    by their name (e.g., "Luke Skywalker", "Darth Vader").
    """
    return await _search_swapi("people", name)


# FILE HANDLER TOOL
@mcp_server.tool()
async def write_to_file(data: str, include_timestamp: bool = True) -> bool:
    """
    Writes data to the dummy_db.txt file using append mode.

    Args:
        data: The string data to write to the file
        include_timestamp: Whether to include a timestamp with the entry (default: True)

    Returns:
        True if write was successful, False otherwise
    """
    handler = FileHandler()
    return handler.write_data(data, include_timestamp)


# --- Main entrypoint to run the server ---
if __name__ == "__main__":
    from config.app import fastapi_app

    print("Starting Star Wars HoloNet MCP Server...")
    print("Visit http://127.0.0.1:8000/mcp/docs for the MCP tool documentation.")
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
