"""
problem_generator.py — Agent 1: Sinh danh sách bài toán theo chủ đề.

Output schema:
[
  {"id": int, "level": "biết|hiểu|vận_dụng", "question": str, "hint": str},
  ...
]
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
    PROBLEMS_PER_SESSION,
)
from utils import extract_json

_AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_AGENTS_DIR)
_PROMPTS_DIR = os.path.join(_BACKEND_DIR, "prompts")


class ProblemGenerator:
    """Agent 1: Sinh danh sách bài toán từ một chủ đề."""

    def __init__(self):
        self.client = Groq(
            api_key=get_groq_api_key(),
            timeout=float(LLM_TIMEOUT_SECONDS),
        )
        _env = Environment(loader=FileSystemLoader(_PROMPTS_DIR))
        self._template = _env.get_template("problem_generator.j2")

    def generate(self, topic: dict) -> list[dict]:
        """
        Sinh bài toán cho chủ đề topic.

        Args:
            topic: dict với keys id, name, description, knowledge

        Returns:
            list of problem dicts với keys id, level, question, hint

        Raises:
            RuntimeError: nếu thất bại sau LLM_MAX_RETRIES lần thử
        """
        prompt = self._template.render(
            topic=topic,
            num_problems=PROBLEMS_PER_SESSION,
        )

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
                problems = extract_json(content)

                if not isinstance(problems, list):
                    raise ValueError(f"Output không phải JSON array, got {type(problems)}")
                if len(problems) == 0:
                    raise ValueError("LLM trả về danh sách rỗng")

                return problems

            except (json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                continue  # Thử lại

        raise RuntimeError(
            f"Agent 1 (ProblemGenerator) thất bại sau {LLM_MAX_RETRIES} lần thử. "
            f"Lỗi cuối: {last_error}"
        )
