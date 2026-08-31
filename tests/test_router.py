from agent.router import ToolRouter
from agent.schema import Action


def test_router_dispatches_general_response():
    router = ToolRouter()
    action = Action(action="general_response", params={"text": "hello"})
    result = router.dispatch(action)
    assert result.success is True
    assert result.output == "hello"


def test_router_dispatches_run_python():
    router = ToolRouter()
    action = Action(action="run_python", params={"code": "print(42)"})
    result = router.dispatch(action)
    assert result.success is True
    assert "42" in result.output


def test_router_unknown_action_returns_error_not_exception():
    router = ToolRouter()
    action = Action(action="not_a_real_tool", params={})
    result = router.dispatch(action)
    assert result.success is False
    assert "unknown action" in result.error.lower()


def test_router_tool_exception_is_caught():
    router = ToolRouter()

    class ExplodingTool:
        name = "run_python"

        def run(self, params):
            raise RuntimeError("boom")

    router.register(ExplodingTool())
    action = Action(action="run_python", params={"code": "print(1)"})
    result = router.dispatch(action)
    assert result.success is False
    assert "crashed" in result.error.lower()
