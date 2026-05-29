"""
test_orchestrator_viet.py — Unit test cho OrchestratorViet (pipeline TV end-to-end với mock).
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from orchestrator_viet import OrchestratorViet

# ── Fixture data ───────────────────────────────────────────────────────────────
SAMPLE_TOPIC = {
    "id": "V2",
    "name": "Từ loại",
    "description": "Danh từ/Động từ/Tính từ",
    "skills": ["Nhận biết từ loại", "Đặt câu"],
}

SAMPLE_QUESTIONS = [
    {"id": "q1", "level": "nhận_biết",  "type": "trắc_nghiệm", "question": "Câu hỏi 1", "hint": "Gợi ý 1"},
    {"id": "q2", "level": "thông_hiểu", "type": "tự_luận",      "question": "Câu hỏi 2", "hint": "Gợi ý 2"},
    {"id": "q3", "level": "vận_dụng",   "type": "tự_luận",      "question": "Câu hỏi 3", "hint": "Gợi ý 3"},
]

SAMPLE_EXPLANATION = {
    "question_id": "q1",
    "read_question": "Tóm tắt câu hỏi...",
    "thinking_direction": "Hướng tìm đáp án...",
    "steps": ["Bước 1", "Bước 2"],
    "answer": "Đáp án...",
    "explanation": "Giải thích...",
    "skill_note": "Kỹ năng TV...",
}


class TestOrchestratorViet:

    @patch("orchestrator_viet.VietAnswerExplainer")
    @patch("orchestrator_viet.VietQuestionGenerator")
    def test_run_returns_list(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_QUESTIONS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_EXPLANATION
        mock_exp_class.return_value = mock_exp

        orc = OrchestratorViet()
        results = orc.run(SAMPLE_TOPIC)

        assert isinstance(results, list)
        assert len(results) == 3

    @patch("orchestrator_viet.VietAnswerExplainer")
    @patch("orchestrator_viet.VietQuestionGenerator")
    def test_run_each_item_has_question_and_explanation(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_QUESTIONS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_EXPLANATION
        mock_exp_class.return_value = mock_exp

        orc = OrchestratorViet()
        results = orc.run(SAMPLE_TOPIC)

        for item in results:
            assert "question" in item
            assert "explanation" in item

    @patch("orchestrator_viet.VietAnswerExplainer")
    @patch("orchestrator_viet.VietQuestionGenerator")
    def test_run_calls_generator_once(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_QUESTIONS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_EXPLANATION
        mock_exp_class.return_value = mock_exp

        orc = OrchestratorViet()
        orc.run(SAMPLE_TOPIC)

        mock_gen.generate.assert_called_once_with(SAMPLE_TOPIC)

    @patch("orchestrator_viet.VietAnswerExplainer")
    @patch("orchestrator_viet.VietQuestionGenerator")
    def test_run_calls_explainer_per_question(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_QUESTIONS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_EXPLANATION
        mock_exp_class.return_value = mock_exp

        orc = OrchestratorViet()
        orc.run(SAMPLE_TOPIC)

        assert mock_exp.explain.call_count == len(SAMPLE_QUESTIONS)

    @patch("orchestrator_viet.VietAnswerExplainer")
    @patch("orchestrator_viet.VietQuestionGenerator")
    def test_run_explainer_failure_graceful(self, mock_gen_class, mock_exp_class):
        """Nếu explainer lỗi ở 1 câu, pipeline vẫn trả về kết quả cho các câu còn lại."""
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_QUESTIONS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.side_effect = RuntimeError("API lỗi")
        mock_exp_class.return_value = mock_exp

        orc = OrchestratorViet()
        results = orc.run(SAMPLE_TOPIC)

        # Vẫn trả về đủ số item
        assert len(results) == len(SAMPLE_QUESTIONS)
        # Mỗi item vẫn có question
        for item in results:
            assert "question" in item
            assert item["explanation"] == {}
