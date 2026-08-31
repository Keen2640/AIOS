"""
run_python.py

Executes arbitrary Python code in an isolated subprocess (never via eval()
or exec() in-process) with a hard timeout and captured stdout/stderr.

This is intentionally conservative: no shell=True, no access to the parent
process's memory, and a timeout to prevent runaway/hanging code.
"""

from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

from tools.base import Tool, ToolResult

DEFAULT_TIMEOUT_SECONDS = 10


class RunPythonTool(Tool):
    name = "run_python"
    description = "Executes a snippet of Python code in a sandboxed subprocess and returns stdout/stderr."

    def run(self, params: Dict[str, Any]) -> ToolResult:
        code = params.get("code", "")
        timeout = params.get("timeout", DEFAULT_TIMEOUT_SECONDS)

        if not code.strip():
            return ToolResult(success=False, output="", error="No code provided.")

        # Write to a temp file rather than passing code inline via -c, so
        # multi-line snippets and syntax errors are handled cleanly.
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            tmp_path = Path(f.name)

        try:
            result = subprocess.run(
                [sys.executable, str(tmp_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode == 0:
                return ToolResult(success=True, output=result.stdout.strip())
            return ToolResult(
                success=False,
                output=result.stdout.strip(),
                error=result.stderr.strip() or f"Process exited with code {result.returncode}",
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False, output="", error=f"Execution timed out after {timeout}s."
            )
        finally:
            tmp_path.unlink(missing_ok=True)
