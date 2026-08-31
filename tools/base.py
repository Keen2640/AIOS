"""
base.py

Defines the Tool interface every AIOS tool must implement. This is what
makes the system extensible: adding a new capability means writing one
class that satisfies this contract and registering it with the router --
no changes to the planner, schema, or router internals required.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    """Standardized result envelope returned by every tool execution."""
    success: bool
    output: str
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"success": self.success, "output": self.output, "error": self.error}


class Tool(ABC):
    """Base class for all AIOS tools."""

    #: Unique name matching the "action" field in ACTION_SCHEMA
    name: str = "base_tool"
    #: Human-readable description (also useful for building planner prompts)
    description: str = "Base tool -- override in subclass."

    @abstractmethod
    def run(self, params: Dict[str, Any]) -> ToolResult:
        """Execute the tool with the given (already-validated) params."""
        raise NotImplementedError
