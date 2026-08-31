"""
search_web.py

Performs a web search by opening the user's default browser to a search
results page. Kept deliberately simple (no headless scraping / no API
key requirement) so it works out of the box -- see README roadmap for a
plan to add a proper search API + result-summarization step.
"""

from __future__ import annotations
import urllib.parse
import webbrowser
from typing import Any, Dict

from tools.base import Tool, ToolResult


class SearchWebTool(Tool):
    name = "search_web"
    description = "Opens a web search for the given query in the default browser."

    def run(self, params: Dict[str, Any]) -> ToolResult:
        query = params.get("query", "").strip()

        if not query:
            return ToolResult(success=False, output="", error="No search query provided.")

        url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

        try:
            opened = webbrowser.open(url)
        except Exception as e:  # pragma: no cover - platform dependent
            return ToolResult(success=False, output="", error=str(e))

        if not opened:
            return ToolResult(
                success=False,
                output="",
                error="No browser available to open (headless environment?).",
            )

        return ToolResult(success=True, output=f"Opened search results for: {query}")
