import uvicorn
import httpx
from fastmcp import FastMCP
from typing import Dict, Any

mcp_server = FastMCP()

# --- Constants & Global HTTP Client ---
SWAPI_BASE_URL = "https://swapi.dev/api/"


# --- Helper Function ---
async def _search_swapi(resource: str, search_term: str) -> Dict[str, Any]:
    """
    A DRY (Don't Repeat Yourself) helper to search any SWAPI resource.
    Returns the first result found, or an error dictionary.
    """
    try:
        async with httpx.AsyncClient(base_url=SWAPI_BASE_URL) as client:
            response = await client.get(f"{resource}/", params={"search": search_term})
            response.raise_for_status()  # Raise an exception for 4xx/5xx errors
            data = response.json()

            if data.get("results"):
                # Success! Return the first matching item.
                return data["results"][0]
            else:
                return {"error": f"{resource.capitalize()} not found."}

    except httpx.HTTPStatusError as e:
        return {"error": f"SWAPI error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


# --- TOOL DEFINITIONS (All 5 Levels) ---


# LEVEL 1 TOOL
@mcp_server.tool()
async def get_person_by_name(name: str) -> Dict[str, Any]:
    """
    Fetches information about a specific person from the Star Wars universe
    by their name (e.g., "Luke Skywalker", "Darth Vader").
    """
    return await _search_swapi("people", name)


# LEVEL 2 TOOL
@mcp_server.tool()
async def get_resource_by_url(url: str) -> Dict[str, Any]:
    """
    Fetches a specific resource (like a planet, ship, or person) using its
    full SWAPI URL. This is used to follow relationships from other objects.
    (e.g., "https://swapi.dev/api/planets/1/")
    """

    if not url.startswith(SWAPI_BASE_URL):
        return {"error": "Invalid API URL. Must be a swapi.dev URL."}

    # Make the URL relative for our client
    # e.g., "https://swapi.dev/api/planets/1/" -> "planets/1/"
    relative_url = url.replace(SWAPI_BASE_URL, "")

    try:

        async with httpx.AsyncClient(base_url=SWAPI_BASE_URL) as client:
            response = await client.get(relative_url)
            if response.status_code == 404:
                return {"error": "Resource not found at that URL."}
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"SWAPI error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


# LEVEL 3 TOOLS
@mcp_server.tool()
async def get_film_by_title(title: str) -> Dict[str, Any]:
    """
    Fetches information about a specific film from the Star Wars saga
    by its title (e.g., "A New Hope", "The Empire Strikes Back").
    """
    return await _search_swapi("films", title)


@mcp_server.tool()
async def get_starship_by_name(name: str) -> Dict[str, Any]:
    """
    Fetches information about a specific starship from the Star Wars universe
    by its name (e.g., "Millennium Falcon", "X-Wing").
    """
    return await _search_swapi("starships", name)


# LEVEL 4 TOOLS
@mcp_server.tool()
async def get_vehicle_by_name(name: str) -> Dict[str, Any]:
    """
    Fetches information about a specific vehicle from the Star Wars universe
    by its name (e.g., "Snowspeeder", "AT-AT").
    """
    return await _search_swapi("vehicles", name)


@mcp_server.tool()
async def get_planet_by_name(name: str) -> Dict[str, Any]:
    """
    Fetches information about a specific planet from the Star Wars universe
    by its name (e.e., "Tatooine", "Hoth").
    """
    return await _search_swapi("planets", name)


# LEVEL 5: SYSTEM PROMPT
# Set the final, comprehensive system prompt for the MCP server.
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

# --- Main entrypoint to run the server ---
if __name__ == "__main__":
    from config.app import fastapi_app

    print("Starting Star Wars HoloNet MCP Server...")
    print("Visit http://127.0.0.1:8000/mcp/docs for the MCP tool documentation.")
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
