from mcp.server.mcpserver import MCPServer
import httpx
import os
import urllib.parse

# Initialize MCPServer server
mcp = MCPServer("bakalari-mcp")

def get_base_url():
    url = os.environ.get("BAKALARI_URL")
    if not url:
        raise ValueError("BAKALARI_URL environment variable is not set.")
    return url.rstrip('/')

def get_credentials():
    username = os.environ.get("BAKALARI_USERNAME")
    password = os.environ.get("BAKALARI_PASSWORD")
    if not username or not password:
        raise ValueError("BAKALARI_USERNAME and BAKALARI_PASSWORD environment variables must be set.")
    return username, password

def get_client():
    return httpx.Client(base_url=get_base_url(), timeout=30.0)

def authenticate(client: httpx.Client) -> str:
    """Returns access token."""
    # Try to login
    username, password = get_credentials()
    data = {
        "client_id": "ANDR",
        "grant_type": "password",
        "username": username,
        "password": password
    }
    
    response = client.post("/api/login", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    response.raise_for_status()
    result = response.json()
    return result["access_token"]

def request_api(endpoint: str, params: dict = None) -> dict:
    with get_client() as client:
        token = authenticate(client)
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = client.get(f"/api/3/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
def get_user() -> dict:
    """Get the current user's information and profile from Bakalari."""
    return request_api("user")

@mcp.tool()
def get_marks() -> dict:
    """Get the current user's marks/grades from Bakalari."""
    return request_api("marks")

@mcp.tool()
def get_timetable_actual() -> dict:
    """Get the current user's actual timetable for this week from Bakalari."""
    return request_api("timetable/actual")

@mcp.tool()
def get_timetable_permanent() -> dict:
    """Get the current user's permanent timetable from Bakalari."""
    return request_api("timetable/permanent")

@mcp.tool()
def get_homeworks() -> dict:
    """Get the current user's homeworks from Bakalari."""
    return request_api("homeworks")

@mcp.tool()
def get_subjects() -> dict:
    """Get the current user's subjects from Bakalari."""
    return request_api("subjects")

@mcp.tool()
def get_events() -> dict:
    """Get the current user's events from Bakalari."""
    return request_api("events")

@mcp.tool()
def get_absence() -> dict:
    """Get the current user's absence from Bakalari."""
    return request_api("absence/student")

@mcp.tool()
def get_messages_received() -> dict:
    """Get the current user's received messages (Komens) from Bakalari."""
    return request_api("komens/messages/received")

@mcp.tool()
def get_messages_sent() -> dict:
    """Get the current user's sent messages (Komens) from Bakalari."""
    return request_api("komens/messages/sent")

@mcp.tool()
def get_noticeboard() -> dict:
    """Get the current user's noticeboard (nastenka) messages from Bakalari."""
    return request_api("komens/messages/noticeboard")

if __name__ == "__main__":
    mcp.run(transport="stdio")
