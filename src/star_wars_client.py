import httpx
from typing import Dict, Any

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
