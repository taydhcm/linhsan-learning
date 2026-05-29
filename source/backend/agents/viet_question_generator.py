"""
viet_question_generator.py — Agent 1 Tiếng Việt: Sinh danh sách câu hỏi ôn tập theo chủ đề.

Output schema:
[
  {
    "id": int,
    "level": "nhận_biết|thông_hiểu|vận_dụng",
    "type": "trắc_nghiệm|tự_luận|điền_chỗ_trống",
    "question": str,
    "hint": str
  },
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

_VALID_LEVELS = {"nhận_biết", "thông_hiểu", "vận_dụng"}
_VALID_TYPES = {"trắc_nghiệm", "tự_luận", "điền_chỗ_trống"}


class VietQuestionGenerator:
    """Agent 1 Tiếng Việt: Sinh danh sách câu hỏi ôn tập từ một chủ đề TV."""

    def __init__(self):
        self.client = Groq(
            api_key=get_groq_api_key(),
            timeout=float(LLM_TIMEOUT_SECONDS),
        )
        _env = Environment(loader=FileSystemLoader(_PROMPTS_DIR))
        self._template = _env.get_template("viet_question_generator.j2")

    def generate(self, topic: dict) -> list[dict]:
        """
        Sinh câu hỏi ôn tập Tiếng Việt cho chủ đề topic.

        Args:
            topic: dict với keys id, name, description, skills

        Returns:
            list of question dicts với keys id, level, type, question, hint

        Raises:
            RuntimeError: nếu thất bại sau LLM_MAX_RETRIES lần thử
        """
        prompt = self._template.render(
            topic=topic,
            num_questions=PROBLEMS_PER_SESSION,
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
                questions = extract_json(content)

                if not isinstance(questions, list):
                    raise ValueError(f"Output không phải JSON array, got {type(questions)}")
                if len(questions) == 0:
                    raise ValueError("LLM trả về danh sách rỗng")

                # Validate từng câu hỏi
                for q in questions:
                    if not isinstance(q, dict):
                        raise ValueError("Mỗi item phải là dict")
                    missing = {"id", "level", "type", "question", "hint"} - q.keys()
                    if missing:
                        raise ValueError(f"Câu hỏi thiếu fields: {missing}")

                return questions

            except (json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                continue  # Thử lại

        raise RuntimeError(
            f"Agent 1 TV (VietQuestionGenerator) thất bại sau {LLM_MAX_RETRIES} lần thử. "
            f"Lỗi cuối: {last_error}"
        )
