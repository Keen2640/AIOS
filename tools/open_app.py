"""
open_app.py

Opens a native application on macOS via the `open -a` system command.
A small allow-by-pattern check is applied to reject obviously malformed
or path-traversal-style input before it ever reaches subprocess.
"""

from __future__ import annotations
import platform
import re
import subprocess
from typing import Any, Dict

from tools.base import Tool, ToolResult

# Application names should just be words/spaces/basic punctuation --
# reject anything that looks like a shell injection attempt or a path.
_SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9 .\-']{1,64}$")


class OpenAppTool(Tool):
    name = "open_app"
    description = "Opens a native macOS application by name."

    def run(self, params: Dict[str, Any]) -> ToolResult:
        app_name = params.get("name", "").strip()

        if not app_name:
            return ToolResult(success=False, output="", error="No application name provided.")

        if not _SAFE_NAME_RE.match(app_name):
            return ToolResult(
                success=False,
                output="",
                error=f"Rejected unsafe application name: {app_name!r}",
            )

        if platform.system() != "Darwin":
            return ToolResult(
                success=False,
                output="",
                error="open_app currently only supports macOS. "
                "See README roadmap for cross-platform support.",
            )

        try:
            subprocess.run(["open", "-a", app_name], check=True, capture_output=True, text=True)
            return ToolResult(success=True, output=f"Opened application: {app_name}")
        except subprocess.CalledProcessError as e:
            return ToolResult(
                success=False,
                output="",
                error=f"Could not open '{app_name}': {e.stderr.strip() or e}",
            )
