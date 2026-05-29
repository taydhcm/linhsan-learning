"""
test_utils.py — Unit test cho utils.py
"""
import json
import pytest
from utils import extract_json, safe_json_parse


class TestExtractJson:
    def test_parse_raw_json_array(self):
        text = '[{"id": 1, "level": "biết"}]'
        result = extract_json(text)
        assert isinstance(result, list)
        assert result[0]["level"] == "biết"

    def test_parse_json_in_code_block(self):
        text = '```json\n[{"id": 1}]\n```'
        result = extract_json(text)
        assert result[0]["id"] == 1

    def test_parse_json_in_code_block_no_lang(self):
        text = '```\n{"key": "value"}\n```'
        result = extract_json(text)
        assert result["key"] == "value"

    def test_parse_raw_json_object(self):
        text = '{"answer": "42", "steps": ["Bước 1"]}'
        result = extract_json(text)
        assert result["answer"] == "42"
        assert len(result["steps"]) == 1

    def test_raises_on_invalid_json(self):
        with pytest.raises(json.JSONDecodeError):
            extract_json("này không phải JSON")

    def test_strips_whitespace(self):
        text = "  \n  [1, 2, 3]  \n  "
        result = extract_json(text)
        assert result == [1, 2, 3]


class TestSafeJsonParse:
    def test_returns_parsed_on_valid(self):
        result = safe_json_parse('{"x": 1}')
        assert result == {"x": 1}

    def test_returns_fallback_on_invalid(self):
        result = safe_json_parse("invalid", fallback=[])
        assert result == []

    def test_returns_none_fallback_by_default(self):
        result = safe_json_parse("bad json")
        assert result is None
