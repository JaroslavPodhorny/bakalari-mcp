# Bakaláři MCP Server

This is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server made by antigravity that allows AI assistants (like Claude Desktop) to connect to the [Bakaláři](https://bakalari.cz/) school information system. 

It provides tools for AI models to safely and automatically fetch your actual timetable, grades, homework, and Komens messages directly from your school's API.

## Features & Available Tools

- `get_user()`: Fetches basic user profile and school information.
- `get_marks()`: Retrieves current grades, weights, and detailed mark info.
- `get_timetable_actual()`: Gets the live timetable for the current week (including substitutions).
- `get_timetable_permanent()`: Gets the permanent/standard timetable.
- `get_homeworks()`: Fetches assigned homeworks.
- `get_subjects()`: Retrieves a list of enrolled subjects.
- `get_events()`: Retrieves school events and calendar entries.
- `get_absence()`: Gets student absence records.
- `get_messages_received()`: Fetches received messages in the Komens module.
- `get_messages_sent()`: Fetches sent messages in the Komens module.
- `get_noticeboard()`: Retrieves noticeboard (nástěnka) messages.

## Prerequisites
- Python >= 3.11
- `uv` package manager (recommended)

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set environment variables with your Bakaláři credentials:
   - `BAKALARI_URL`: The URL of your school's Bakaláři instance (e.g., `https://bakalari.skola.cz`)
   - `BAKALARI_USERNAME`: Your login username
   - `BAKALARI_PASSWORD`: Your login password

## Configuring AI Assistants (e.g., Claude Desktop)

To use this with Claude Desktop, add the following to your `claude_desktop_config.json` (settings -> developer -> edit config):

```json
{
  "mcpServers": {
    "bakalari": {
      "command": "/path/to/your/uv",
      "args": [
        "--directory",
        "/absolute/path/to/bakalari-mcp",
        "run",
        "server.py"
      ],
      "env": {
        "BAKALARI_URL": "https://bakalari.skola.cz",
        "BAKALARI_USERNAME": "your_username",
        "BAKALARI_PASSWORD": "your_password"
      }
    }
  }
}
```

*Note: You must use the absolute path to the `uv` executable (e.g., `/Users/yourusername/.local/bin/uv`) instead of just `"uv"` in desktop graphical applications.*

## Testing manually

You can run the server directly via `uv` or standard Python. Since it uses MCP over standard input/output, running it directly in a terminal will start the server and it will wait for MCP JSON-RPC messages on stdin.

```bash
uv run server.py
```
