import json
import pytest

from agent.schema import validate_action, ActionValidationError


def test_valid_run_python_action():
    raw = json.dumps({"action": "run_python", "params": {"code": "print(1+1)"}})
    action = validate_action(raw)
    assert action.action == "run_python"
    assert action.params["code"] == "print(1+1)"


def test_valid_open_app_action():
    raw = {"action": "open_app", "params": {"name": "Safari"}}
    action = validate_action(raw)
    assert action.action == "open_app"
    assert action.params["name"] == "Safari"


def test_valid_general_response_action():
    raw = {"action": "general_response", "params": {"text": "Hi there!"}}
    action = validate_action(raw)
    assert action.params["text"] == "Hi there!"


def test_invalid_json_raises():
    with pytest.raises(ActionValidationError):
        validate_action("this is not json")


def test_unknown_action_raises():
    raw = {"action": "delete_everything", "params": {}}
    with pytest.raises(ActionValidationError):
        validate_action(raw)


def test_missing_required_param_raises():
    # run_python requires "code" -- omitted here
    raw = {"action": "run_python", "params": {}}
    with pytest.raises(ActionValidationError):
        validate_action(raw)


def test_additional_top_level_properties_rejected():
    raw = {
        "action": "general_response",
        "params": {"text": "hi"},
        "unexpected_field": "nope",
    }
    with pytest.raises(ActionValidationError):
        validate_action(raw)
