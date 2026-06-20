import os
import subprocess
import webbrowser
import json

# -------------------------
# TOOL: run python code
# -------------------------
def run_python(code: str):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return {"status": "success", "output": "Code executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------
# TOOL: open apps / files
# -------------------------
def open_app(app_name: str):
    try:
        subprocess.run(["open", "-a", app_name])
        return {"status": "success", "app": app_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------
# TOOL: web search
# -------------------------
def search_web(query: str):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return {"status": "success", "query": query}

# -------------------------
# TOOL ROUTER
# -------------------------
def execute_tool(action: dict):
    tool = action.get("action")
    input_data = action.get("input")

    if tool == "run_python":
        return run_python(input_data)

    elif tool == "open_app":
        return open_app(input_data)

    elif tool == "search_web":
        return search_web(input_data)

    elif tool == "general_response":
        return {"status": "ok", "response": input_data}

    else:
        return {"status": "error", "message": "Unknown tool"}