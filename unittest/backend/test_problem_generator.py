"""
test_problem_generator.py — Unit test cho Agent 1 (ProblemGenerator).
Dùng mock — không gọi Groq API thật.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from agents.problem_generator import ProblemGenerator

# ── Fixture data ───────────────────────────────────────────────────────────────
T1_TOPIC = {
    "id": "T1",
    "name": "Số tự nhiên",
    "description": "Đọc/viết số đến 1 000 000",
    "knowledge": ["Đọc và viết số tự nhiên đến 1 000 000"],
}

SAMPLE_PROBLEMS = [
    {"id": 1, "level": "biết",     "question": "Viết số 345 678 bằng chữ?",       "hint": "Đọc từng hàng."},
    {"id": 2, "level": "hiểu",     "question": "Chữ số 4 trong 345 678 có giá trị bao nhiêu?", "hint": "Nhìn vào vị trí hàng."},
    {"id": 3, "level": "vận_dụng", "question": "Một trường có 1 234 học sinh. Làm tròn đến hàng trăm.", "hint": "Nhìn chữ số hàng chục."},
    {"id": 4, "level": "biết",     "question": "So sánh: 456 789 ○ 456 879?",     "hint": "So sánh từng hàng."},
    {"id": 5, "level": "hiểu",     "question": "Sắp xếp các số sau theo thứ tự tăng dần.",     "hint": "Bắt đầu từ hàng cao nhất."},
    {"id": 6, "level": "vận_dụng", "question": "Một nhà máy sản xuất 125 000 sản phẩm. Làm tròn đến hàng nghìn.", "hint": "Nhìn hàng trăm."},
]


def _make_mock_groq(content: str):
    """Helper tạo mock Groq client trả về content cho trước."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestProblemGenerator:

    @patch("agents.problem_generator.Groq")
    def test_generate_returns_list(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_PROBLEMS))

        gen = ProblemGenerator()
        result = gen.generate(T1_TOPIC)

        assert isinstance(result, list)
        assert len(result) == 6

    @patch("agents.problem_generator.Groq")
    def test_generate_has_required_fields(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_PROBLEMS))

        gen = ProblemGenerator()
        result = gen.generate(T1_TOPIC)

        for problem in result:
            assert "id" in problem
            assert "level" in problem
            assert "question" in problem
            assert "hint" in problem

    @patch("agents.problem_generator.Groq")
    def test_generate_has_all_levels(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_PROBLEMS))

        gen = ProblemGenerator()
        result = gen.generate(T1_TOPIC)

        levels = {p["level"] for p in result}
        assert "biết" in levels
        assert "hiểu" in levels
        assert "vận_dụng" in levels

    @patch("agents.problem_generator.Groq")
    def test_generate_handles_json_in_code_block(self, mock_groq_class):
        """LLM thường wrap JSON trong markdown code block — phải parse được."""
        content = f"```json\n{json.dumps(SAMPLE_PROBLEMS)}\n```"
        mock_groq_class.return_value = _make_mock_groq(content)

        gen = ProblemGenerator()
        result = gen.generate(T1_TOPIC)
        assert len(result) == 6

    @patch("agents.problem_generator.Groq")
    def test_generate_retries_on_invalid_json(self, mock_groq_class):
        """Phải retry và thành công ở lần thử thứ 2."""
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        bad_response = MagicMock()
        bad_response.choices[0].message.content = "không phải JSON"

        good_response = MagicMock()
        good_response.choices[0].message.content = json.dumps(SAMPLE_PROBLEMS)

        # Lần 1 trả bad, lần 2 trả good
        mock_client.chat.completions.create.side_effect = [bad_response, good_response]

        gen = ProblemGenerator()
        result = gen.generate(T1_TOPIC)
        assert isinstance(result, list)
        assert mock_client.chat.completions.create.call_count == 2

    @patch("agents.problem_generator.Groq")
    def test_generate_raises_after_max_retries(self, mock_groq_class):
        """Sau MAX_RETRIES lần thất bại phải raise RuntimeError."""
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        bad_response = MagicMock()
        bad_response.choices[0].message.content = "luôn luôn sai"
        mock_client.chat.completions.create.return_value = bad_response

        gen = ProblemGenerator()
        with pytest.raises(RuntimeError, match="Agent 1"):
            gen.generate(T1_TOPIC)
