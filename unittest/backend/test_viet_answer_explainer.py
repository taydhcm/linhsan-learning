"""
test_viet_answer_explainer.py — Unit test cho Agent 2 TV (VietAnswerExplainer).
Dùng mock — không gọi Groq API thật.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from agents.viet_answer_explainer import VietAnswerExplainer

# ── Fixture data ───────────────────────────────────────────────────────────────
SAMPLE_QUESTION = {
    "id": "q1",
    "level": "nhận_biết",
    "type": "trắc_nghiệm",
    "question": "Từ nào là danh từ: chạy, nhà, đẹp, ăn?",
    "hint": "Danh từ chỉ sự vật.",
}

SAMPLE_EXPLANATION = {
    "question_id": "q1",
    "read_question": "Câu này hỏi mình tìm từ chỉ sự vật trong 4 từ đã cho.",
    "thinking_direction": "Chúng mình sẽ nhớ lại danh từ là gì rồi kiểm tra từng từ.",
    "steps": [
        "Bước 1: Danh từ là từ chỉ người, vật, nơi chốn.",
        "Bước 2: 'chạy' là hoạt động → động từ.",
        "Bước 3: 'nhà' là vật → danh từ ✓",
        "Bước 4: 'đẹp' là đặc điểm → tính từ.",
        "Bước 5: 'ăn' là hoạt động → động từ.",
    ],
    "answer": "Đáp án: 'nhà' — vì nhà chỉ sự vật (nơi chốn).",
    "explanation": "Giống như khi mình nói 'ngôi nhà của em' — nhà là thứ mình có thể thấy, chạm vào. Còn 'chạy', 'ăn' là việc mình làm.",
    "skill_note": "Kỹ năng: Nhận biết danh từ bằng cách hỏi 'đây là gì?' hoặc 'ai/cái gì?'.",
}


def _make_mock_groq(content: str):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestVietAnswerExplainer:

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_returns_dict(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_EXPLANATION))

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        assert isinstance(result, dict)

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_has_all_required_fields(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_EXPLANATION))

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        required = {
            "question_id", "read_question", "thinking_direction",
            "steps", "answer", "explanation", "skill_note",
        }
        assert required.issubset(result.keys())

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_steps_is_non_empty_list(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_EXPLANATION))

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        assert isinstance(result["steps"], list)
        assert len(result["steps"]) > 0

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_answer_not_empty(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_EXPLANATION))

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        assert result["answer"].strip() != ""

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_skill_note_not_empty(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_EXPLANATION))

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        assert result["skill_note"].strip() != ""

    @patch("agents.viet_answer_explainer.Groq")
    def test_explain_handles_json_in_code_block(self, mock_groq_class):
        """LLM đôi khi wrap JSON trong markdown code block."""
        content = f"```json\n{json.dumps(SAMPLE_EXPLANATION)}\n```"
        mock_groq_class.return_value = _make_mock_groq(content)

        exp = VietAnswerExplainer()
        result = exp.explain(SAMPLE_QUESTION)

        assert isinstance(result, dict)
        assert result["answer"].strip() != ""
