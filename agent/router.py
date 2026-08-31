"""
router.py

Maps a validated Action to its registered Tool implementation and executes
it. The router has zero knowledge of tool internals -- it only relies on
the Tool interface contract, which is what makes new tools pluggable
without touching this file.
"""

from __future__ import annotations
from typing import Dict

from agent.schema import Action
from agent.logger import get_logger
from tools.base import Tool, ToolResult
from tools.run_python import RunPythonTool
from tools.open_app import OpenAppTool
from tools.search_web import SearchWebTool
from tools.general_response import GeneralResponseTool

logger = get_logger(__name__)


class ToolRouter:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        for tool in (RunPythonTool(), OpenAppTool(), SearchWebTool(), GeneralResponseTool()):
            self.register(tool)

    def register(self, tool: Tool) -> None:
        """Register a new tool. Later registrations override earlier ones
        with the same name, so this also supports swapping implementations."""
        self._tools[tool.name] = tool
        logger.debug("Registered tool: %s", tool.name)

    def dispatch(self, action: Action) -> ToolResult:
        tool = self._tools.get(action.action)
        if tool is None:
            logger.error("No tool registered for action: %s", action.action)
            return ToolResult(
                success=False,
                output="",
                error=f"Unknown action '{action.action}' -- no tool registered.",
            )

        logger.info("Dispatching action=%s params=%s", action.action, action.params)
        try:
            result = tool.run(action.params)
        except Exception as e:  # Defense in depth: a tool bug should never crash the agent loop
            logger.exception("Tool '%s' raised an unhandled exception", tool.name)
            result = ToolResult(success=False, output="", error=f"Tool crashed: {e}")

        logger.info(
            "Result for action=%s success=%s error=%s",
            action.action,
            result.success,
            result.error,
        )
        return result
