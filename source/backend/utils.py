"""
utils.py — Helper functions: JSON parsing, retry logic.
"""

import json
import re
from typing import Any


def extract_json(text: str) -> Any:
    """
    Trích xuất và parse JSON từ LLM response.
    Xử lý cả trường hợp LLM wrap JSON trong markdown code block.
    """
    # Thử tìm JSON trong code block ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    else:
        text = text.strip()

    return json.loads(text)


def safe_json_parse(text: str, fallback: Any = None) -> Any:
    """Parse JSON an toàn, trả về fallback nếu có lỗi."""
    try:
        return extract_json(text)
    except (json.JSONDecodeError, AttributeError, TypeError):
        return fallback
