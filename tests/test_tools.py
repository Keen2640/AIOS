from tools.run_python import RunPythonTool
from tools.general_response import GeneralResponseTool
from tools.open_app import OpenAppTool
from tools.search_web import SearchWebTool


def test_run_python_success():
    tool = RunPythonTool()
    result = tool.run({"code": "print('hello from aios')"})
    assert result.success is True
    assert "hello from aios" in result.output


def test_run_python_syntax_error_reported():
    tool = RunPythonTool()
    result = tool.run({"code": "def broken(:\n  pass"})
    assert result.success is False
    assert result.error  # some error message captured from stderr


def test_run_python_timeout():
    tool = RunPythonTool()
    result = tool.run({"code": "import time; time.sleep(5)", "timeout": 1})
    assert result.success is False
    assert "timed out" in result.error.lower()


def test_run_python_empty_code_rejected():
    tool = RunPythonTool()
    result = tool.run({"code": ""})
    assert result.success is False


def test_general_response_returns_text():
    tool = GeneralResponseTool()
    result = tool.run({"text": "Just chatting, no action needed."})
    assert result.success is True
    assert result.output == "Just chatting, no action needed."


def test_general_response_empty_text_rejected():
    tool = GeneralResponseTool()
    result = tool.run({"text": ""})
    assert result.success is False


def test_open_app_rejects_unsafe_name():
    tool = OpenAppTool()
    result = tool.run({"name": "Safari; rm -rf /"})
    assert result.success is False
    assert "unsafe" in result.error.lower()


def test_open_app_rejects_empty_name():
    tool = OpenAppTool()
    result = tool.run({"name": ""})
    assert result.success is False


def test_search_web_rejects_empty_query():
    tool = SearchWebTool()
    result = tool.run({"query": ""})
    assert result.success is False
