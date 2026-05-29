"""
solution_explainer.py — Agent 2: Giải và giải thích bài toán theo cách trẻ em hiểu.

Output schema:
{
  "problem_id": int,
  "read_problem": str,
  "thinking_direction": str,
  "steps": [str, ...],
  "answer": str,
  "explanation": str,
  "skill_note": str
}
"""

import os
import json
from groq import Groq
from jinja2 import Environment, FileSystemLoader

from config import (
    get_groq_api_key,
    LLM_MODEL_PRIMARY,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
    LLM_TIMEOUT_SECONDS,
    LLM_MAX_RETRIES,
)
from utils import extract_json

_AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_AGENTS_DIR)
_PROMPTS_DIR = os.path.join(_BACKEND_DIR, "prompts")

_REQUIRED_FIELDS = {
    "problem_id", "read_problem", "thinking_direction",
    "steps", "answer", "explanation", "skill_note",
}


class SolutionExplainer:
    """Agent 2: Giải và giải thích bài toán theo cách trẻ em hiểu."""

    def __init__(self):
        self.client = Groq(
            api_key=get_groq_api_key(),
            timeout=float(LLM_TIMEOUT_SECONDS),
        )
        _env = Environment(loader=FileSystemLoader(_PROMPTS_DIR))
        self._template = _env.get_template("solution_explainer.j2")

    def explain(self, problem: dict) -> dict:
        """
        Giải và giải thích một bài toán.

        Args:
            problem: dict với keys id, level, question, hint

        Returns:
            dict với keys: problem_id, read_problem, thinking_direction,
                           steps, answer, explanation, skill_note

        Raises:
            RuntimeError: nếu thất bại sau LLM_MAX_RETRIES lần thử
        """
        prompt = self._template.render(problem=problem)

        last_error: Exception | None = None
        for attempt in range(LLM_MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=LLM_MODEL_PRIMARY,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=LLM_MAX_TOKENS,
                    temperature=LLM_TEMPERATURE,
                )
                content = response.choices[0].message.content
                solution = extract_json(content)

                if not isinstance(solution, dict):
                    raise ValueError(f"Output không phải JSON object, got {type(solution)}")

                missing = _REQUIRED_FIELDS - solution.keys()
                if missing:
                    raise ValueError(f"Thiếu fields: {missing}")

                return solution

            except (json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                continue  # Thử lại

        raise RuntimeError(
            f"Agent 2 (SolutionExplainer) thất bại sau {LLM_MAX_RETRIES} lần thử. "
            f"Lỗi cuối: {last_error}"
        )
