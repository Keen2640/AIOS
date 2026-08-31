"""
planner.py

The LLM planning layer. Takes raw natural-language user input, prompts
Gemini to produce a single JSON action conforming to ACTION_SCHEMA, and
hands the raw text off to validate_action() before anything downstream
ever sees it.

The prompt itself does two jobs:
  1. Describes each available tool (kept in sync with tools/*.py via the
     TOOL_DESCRIPTIONS list below) so the model knows what it can do.
  2. Forces strict JSON-only output -- no prose, no markdown fences --
     since the parser has zero tolerance for anything else.
"""

from __future__ import annotations
import os
from typing import Optional

from agent.schema import Action, ActionValidationError, validate_action
from agent.logger import get_logger

logger = get_logger(__name__)

TOOL_DESCRIPTIONS = """
Available actions:

1. run_python
   params: {"code": "<python source as a string>"}
   Use for calculations, data processing, or any task best solved by executing code.

2. open_app
   params: {"name": "<macOS application name, e.g. 'Visual Studio Code'>"}
   Use when the user wants to open/launch a native application.

3. search_web
   params: {"query": "<search query string>"}
   Use when the user wants information looked up online.

4. general_response
   params: {"text": "<plain text reply>"}
   Use when the request is conversational, ambiguous, or doesn't map to
   any of the above -- NEVER force one of the other actions if you are
   not confident it's what the user wants.
"""

SYSTEM_PROMPT = f"""You are the planning layer of AIOS, an agent that controls a local computer.

Given a user's natural-language request, respond with EXACTLY ONE JSON object
and nothing else -- no markdown code fences, no explanation text outside the JSON.

{TOOL_DESCRIPTIONS}

Required JSON shape:
{{"action": "<one of the action names above>", "params": {{...}}, "reasoning": "<one short sentence>"}}

If you are not confident the request maps cleanly to run_python, open_app, or
search_web, use general_response instead of guessing.
"""


class PlannerError(Exception):
    """Raised when the planner cannot produce a valid action after retries."""


class GeminiPlanner:
    """
    Wraps the Gemini API call + validation retry loop.

    Requires the `google-generativeai` package and a GEMINI_API_KEY
    environment variable (see .env.example).
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", max_retries: int = 2) -> None:
        self.model_name = model_name
        self.max_retries = max_retries
        self._model = None  # lazy-initialized so importing this module never requires an API key

    def _get_model(self):
        if self._model is not None:
            return self._model

        try:
            import google.generativeai as genai
        except ImportError as e:
            raise PlannerError(
                "google-generativeai is not installed. Run: pip install google-generativeai"
            ) from e

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise PlannerError(
                "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
            )

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SYSTEM_PROMPT,
        )
        return self._model

    def plan(self, user_input: str) -> Action:
        """
        Sends user_input to the LLM and returns a validated Action.

        Retries up to `max_retries` times if the model's output fails JSON
        parsing or schema validation, appending the error to the next
        prompt so the model can self-correct.
        """
        model = self._get_model()
        last_error: Optional[str] = None

        for attempt in range(1, self.max_retries + 2):
            prompt = user_input
            if last_error:
                prompt = (
                    f"{user_input}\n\n"
                    f"(Your previous response was invalid: {last_error}. "
                    f"Respond again with ONLY a valid JSON object matching the schema.)"
                )

            logger.debug("Planner attempt %d for input: %r", attempt, user_input)
            response = model.generate_content(prompt)
            raw_text = (response.text or "").strip()

            # Strip accidental markdown fences defensively, even though the
            # prompt explicitly forbids them.
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`")
                if raw_text.lower().startswith("json"):
                    raw_text = raw_text[4:].strip()

            try:
                return validate_action(raw_text)
            except ActionValidationError as e:
                logger.warning("Planner output failed validation (attempt %d): %s", attempt, e)
                last_error = str(e)

        raise PlannerError(
            f"Planner failed to produce a valid action after {self.max_retries + 1} attempts. "
            f"Last error: {last_error}"
        )
