"""
general_response.py

Safe fallback tool. When the planner determines a request is ambiguous,
purely conversational, or doesn't map to a supported action, it returns
this action instead of forcing a best-guess execution. This is a key
safety property of AIOS: the system never "hallucinates" an action for
input it doesn't understand.
"""

from __future__ import annotations
from typing import Any, Dict

from tools.base import Tool, ToolResult


class GeneralResponseTool(Tool):
    name = "general_response"
    description = "Returns a plain-text response without executing any system action."

    def run(self, params: Dict[str, Any]) -> ToolResult:
        text = params.get("text", "").strip()
        if not text:
            return ToolResult(success=False, output="", error="No response text provided.")
        return ToolResult(success=True, output=text)
