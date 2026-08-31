"""
main.py

AIOS entry point. Runs the full agent loop:

    user input -> planner (LLM) -> schema validation -> tool router -> logger

Run with:
    python main.py
"""

from __future__ import annotations
import sys

from dotenv import load_dotenv

from agent.planner import GeminiPlanner, PlannerError
from agent.schema import ActionValidationError
from agent.router import ToolRouter
from agent.logger import get_logger

logger = get_logger("aios.main")

BANNER = """
╔═══════════════════════════════════════════╗
║   AIOS — AI Agent Operating System         ║
║   Type a request in plain English.         ║
║   Type 'exit' or 'quit' to stop.           ║
╚═══════════════════════════════════════════╝
"""


def run_repl() -> None:
    load_dotenv()

    planner = GeminiPlanner()
    router = ToolRouter()

    print(BANNER)

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting AIOS.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting AIOS.")
            break

        try:
            action = planner.plan(user_input)
        except PlannerError as e:
            logger.error("Planning failed: %s", e)
            print(f"[planner error] {e}")
            continue
        except ActionValidationError as e:
            logger.error("Validation failed: %s", e)
            print(f"[validation error] {e}")
            continue

        print(f"[planned] action={action.action} params={action.params}")
        if action.reasoning:
            print(f"[reasoning] {action.reasoning}")

        result = router.dispatch(action)

        if result.success:
            print(f"[✅ success] {result.output}")
        else:
            print(f"[❌ error] {result.error}")


if __name__ == "__main__":
    try:
        run_repl()
    except Exception:
        logger.exception("Fatal error in AIOS main loop")
        sys.exit(1)
