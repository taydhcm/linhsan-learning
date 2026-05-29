"""
test_solution_explainer.py — Unit test cho Agent 2 (SolutionExplainer).
Dùng mock — không gọi Groq API thật.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from agents.solution_explainer import SolutionExplainer

# ── Fixture data ───────────────────────────────────────────────────────────────
SAMPLE_PROBLEM = {
    "id": 1,
    "level": "biết",
    "question": "Viết số 345 678 bằng chữ?",
    "hint": "Đọc từng hàng từ trái sang phải.",
}

SAMPLE_SOLUTION = {
    "problem_id": 1,
    "read_problem": "Bài hỏi mình viết số 345 678 thành chữ.",
    "thinking_direction": "Chúng mình đọc từng hàng từ trái sang phải nhé!",
    "steps": [
        "Bước 1: Nhìn vào số 345 678.",
        "Bước 2: Đọc phần trước: ba trăm bốn mươi lăm nghìn.",
        "Bước 3: Đọc phần sau: sáu trăm bảy mươi tám.",
        "Bước 4: Ghép lại: ba trăm bốn mươi lăm nghìn sáu trăm bảy mươi tám.",
    ],
    "answer": "Vậy số 345 678 viết bằng chữ là: ba trăm bốn mươi lăm nghìn sáu trăm bảy mươi tám.",
    "explanation": "Giống như khi mình đếm tiền, mình đếm từng tờ to rồi đến tờ nhỏ.",
    "skill_note": "Biết đọc và viết số có nhiều chữ số theo từng lớp.",
}


def _make_mock_groq(content: str):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestSolutionExplainer:

    @patch("agents.solution_explainer.Groq")
    def test_explain_returns_dict(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_SOLUTION))

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)

        assert isinstance(result, dict)

    @patch("agents.solution_explainer.Groq")
    def test_explain_has_all_required_fields(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_SOLUTION))

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)

        required = {
            "problem_id", "read_problem", "thinking_direction",
            "steps", "answer", "explanation", "skill_note",
        }
        for field in required:
            assert field in result, f"Thiếu field: {field}"

    @patch("agents.solution_explainer.Groq")
    def test_explain_steps_is_list(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_SOLUTION))

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)

        assert isinstance(result["steps"], list)
        assert len(result["steps"]) > 0

    @patch("agents.solution_explainer.Groq")
    def test_explain_handles_json_in_code_block(self, mock_groq_class):
        content = f"```json\n{json.dumps(SAMPLE_SOLUTION)}\n```"
        mock_groq_class.return_value = _make_mock_groq(content)

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)
        assert result["problem_id"] == 1

    @patch("agents.solution_explainer.Groq")
    def test_explain_retries_on_invalid_json(self, mock_groq_class):
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        bad = MagicMock()
        bad.choices[0].message.content = "không phải JSON"

        good = MagicMock()
        good.choices[0].message.content = json.dumps(SAMPLE_SOLUTION)

        mock_client.chat.completions.create.side_effect = [bad, good]

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)
        assert isinstance(result, dict)
        assert mock_client.chat.completions.create.call_count == 2

    @patch("agents.solution_explainer.Groq")
    def test_explain_retries_on_missing_fields(self, mock_groq_class):
        """Output thiếu field phải retry."""
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        incomplete = {"problem_id": 1, "answer": "42"}  # thiếu nhiều field

        bad = MagicMock()
        bad.choices[0].message.content = json.dumps(incomplete)

        good = MagicMock()
        good.choices[0].message.content = json.dumps(SAMPLE_SOLUTION)

        mock_client.chat.completions.create.side_effect = [bad, good]

        explainer = SolutionExplainer()
        result = explainer.explain(SAMPLE_PROBLEM)
        assert "skill_note" in result

    @patch("agents.solution_explainer.Groq")
    def test_explain_raises_after_max_retries(self, mock_groq_class):
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        bad = MagicMock()
        bad.choices[0].message.content = "luôn luôn sai"
        mock_client.chat.completions.create.return_value = bad

        explainer = SolutionExplainer()
        with pytest.raises(RuntimeError, match="Agent 2"):
            explainer.explain(SAMPLE_PROBLEM)
