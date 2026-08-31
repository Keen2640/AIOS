"""
schema.py

Defines the strict shape every planner-generated action must satisfy, and
exposes a validate_action() helper used by the router before any
execution is allowed to happen.

This is the core safety boundary of AIOS: raw LLM output is NEVER executed
directly. It must first be parsed as JSON and pass validation here.

Implemented with pure Python (no jsonschema dependency) so the project has
zero external dependencies for its most safety-critical component.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List


class ActionValidationError(Exception):
    """Raised when a planner-generated action fails validation."""


# Required parameter keys per action, and the expected type of each.
_ACTION_SPECS: Dict[str, Dict[str, type]] = {
    "run_python": {"code": str},
    "open_app": {"name": str},
    "search_web": {"query": str},
    "general_response": {"text": str},
}

ALLOWED_ACTIONS: List[str] = list(_ACTION_SPECS.keys())
ALLOWED_TOP_LEVEL_KEYS = {"action", "params", "reasoning"}


@dataclass
class Action:
    action: str
    params: Dict[str, Any]
    reasoning: str = ""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Action":
        return Action(
            action=data["action"],
            params=data.get("params", {}),
            reasoning=data.get("reasoning", ""),
        )


def validate_action(raw: "str | Dict[str, Any]") -> Action:
    """
    Validate a raw planner action (JSON string or dict).

    Enforces:
      - valid JSON (if given as a string)
      - top level is an object with only {"action", "params", "reasoning"}
      - "action" is one of the registered action names
      - "params" is an object containing exactly the required keys for
        that action, with the correct type for each

    Raises:
        ActionValidationError: on any failure above.

    Returns:
        Action: a validated, typed Action object safe to route.
    """
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ActionValidationError(f"Planner output was not valid JSON: {e}") from e
    else:
        data = raw

    if not isinstance(data, dict):
        raise ActionValidationError(f"Top-level action must be a JSON object, got {type(data).__name__}")

    extra_keys = set(data.keys()) - ALLOWED_TOP_LEVEL_KEYS
    if extra_keys:
        raise ActionValidationError(f"Unexpected top-level field(s): {sorted(extra_keys)}")

    if "action" not in data:
        raise ActionValidationError("Missing required field: 'action'")
    if "params" not in data:
        raise ActionValidationError("Missing required field: 'params'")

    action_name = data["action"]
    if action_name not in _ACTION_SPECS:
        raise ActionValidationError(
            f"Unknown action '{action_name}'. Must be one of: {ALLOWED_ACTIONS}"
        )

    params = data["params"]
    if not isinstance(params, dict):
        raise ActionValidationError("'params' must be a JSON object")

    spec = _ACTION_SPECS[action_name]
    for key, expected_type in spec.items():
        if key not in params:
            raise ActionValidationError(f"Action '{action_name}' is missing required param '{key}'")
        if not isinstance(params[key], expected_type):
            raise ActionValidationError(
                f"Param '{key}' for action '{action_name}' must be {expected_type.__name__}, "
                f"got {type(params[key]).__name__}"
            )

    reasoning = data.get("reasoning", "")
    if not isinstance(reasoning, str):
        raise ActionValidationError("'reasoning' must be a string if provided")

    return Action(action=action_name, params=params, reasoning=reasoning)
