"""
test_viet_question_generator.py — Unit test cho Agent 1 TV (VietQuestionGenerator).
Dùng mock — không gọi Groq API thật.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from agents.viet_question_generator import VietQuestionGenerator

# ── Fixture data ───────────────────────────────────────────────────────────────
V2_TOPIC = {
    "id": "V2",
    "name": "Từ loại",
    "description": "Danh từ/Động từ/Tính từ/Đại từ",
    "skills": [
        "Nhận biết danh từ, động từ, tính từ trong câu",
        "Phân loại từ loại theo chức năng",
        "Đặt câu với từ loại cho trước",
    ],
}

SAMPLE_QUESTIONS = [
    {"id": "q1", "level": "nhận_biết",  "type": "trắc_nghiệm",    "question": "Từ nào là danh từ: chạy, nhà, đẹp, ăn?", "hint": "Danh từ chỉ sự vật."},
    {"id": "q2", "level": "nhận_biết",  "type": "điền_chỗ_trống", "question": "Điền từ loại phù hợp: 'học sinh' là ___ từ.", "hint": "Chỉ người."},
    {"id": "q3", "level": "thông_hiểu", "type": "trắc_nghiệm",    "question": "Câu 'Bé chạy nhanh' có động từ là gì?", "hint": "Từ chỉ hoạt động."},
    {"id": "q4", "level": "thông_hiểu", "type": "tự_luận",         "question": "Hãy giải thích tại sao 'đẹp' là tính từ.", "hint": "Nghĩ đến đặc điểm."},
    {"id": "q5", "level": "vận_dụng",   "type": "tự_luận",         "question": "Đặt một câu có cả danh từ và động từ.", "hint": "Ai làm gì."},
    {"id": "q6", "level": "vận_dụng",   "type": "tự_luận",         "question": "Viết đoạn văn 2 câu dùng ít nhất 3 từ loại khác nhau.", "hint": "Kể về buổi sáng."},
]

VALID_LEVELS = {"nhận_biết", "thông_hiểu", "vận_dụng"}
VALID_TYPES  = {"trắc_nghiệm", "tự_luận", "điền_chỗ_trống"}


def _make_mock_groq(content: str):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestVietQuestionGenerator:

    @patch("agents.viet_question_generator.Groq")
    def test_generate_returns_list(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_QUESTIONS))

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        assert isinstance(result, list)
        assert len(result) == 6

    @patch("agents.viet_question_generator.Groq")
    def test_generate_has_required_fields(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_QUESTIONS))

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        for q in result:
            assert "id" in q
            assert "level" in q
            assert "type" in q
            assert "question" in q
            assert "hint" in q

    @patch("agents.viet_question_generator.Groq")
    def test_generate_has_all_3_levels(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_QUESTIONS))

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        levels = {q["level"] for q in result}
        assert levels == VALID_LEVELS

    @patch("agents.viet_question_generator.Groq")
    def test_generate_valid_types(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_QUESTIONS))

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        for q in result:
            assert q["type"] in VALID_TYPES

    @patch("agents.viet_question_generator.Groq")
    def test_generate_handles_json_in_code_block(self, mock_groq_class):
        """LLM đôi khi wrap JSON trong markdown code block."""
        content = f"```json\n{json.dumps(SAMPLE_QUESTIONS)}\n```"
        mock_groq_class.return_value = _make_mock_groq(content)

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        assert isinstance(result, list)
        assert len(result) == 6

    @patch("agents.viet_question_generator.Groq")
    def test_generate_questions_not_empty(self, mock_groq_class):
        mock_groq_class.return_value = _make_mock_groq(json.dumps(SAMPLE_QUESTIONS))

        gen = VietQuestionGenerator()
        result = gen.generate(V2_TOPIC)

        for q in result:
            assert q["question"].strip() != ""
