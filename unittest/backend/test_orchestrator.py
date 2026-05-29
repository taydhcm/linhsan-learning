"""
test_orchestrator.py — Unit test cho Orchestrator (end-to-end pipeline với mock).
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from orchestrator import Orchestrator

# ── Fixture data ───────────────────────────────────────────────────────────────
SAMPLE_TOPIC = {
    "id": "T1",
    "name": "Số tự nhiên",
    "description": "Đọc/viết số đến 1 000 000",
    "knowledge": ["Đọc và viết số tự nhiên"],
}

SAMPLE_PROBLEMS = [
    {"id": 1, "level": "biết",   "question": "Đề bài 1", "hint": "Gợi ý 1"},
    {"id": 2, "level": "hiểu",   "question": "Đề bài 2", "hint": "Gợi ý 2"},
    {"id": 3, "level": "vận_dụng", "question": "Đề bài 3", "hint": "Gợi ý 3"},
]

SAMPLE_SOLUTION = {
    "problem_id": 1,
    "read_problem": "Tóm tắt...",
    "thinking_direction": "Hướng giải...",
    "steps": ["Bước 1", "Bước 2"],
    "answer": "Đáp án...",
    "explanation": "Giải thích...",
    "skill_note": "Kỹ năng...",
}


class TestOrchestrator:

    @patch("orchestrator.SolutionExplainer")
    @patch("orchestrator.ProblemGenerator")
    def test_run_returns_list_of_pairs(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_PROBLEMS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_SOLUTION
        mock_exp_class.return_value = mock_exp

        orchestrator = Orchestrator()
        results = orchestrator.run(SAMPLE_TOPIC)

        assert isinstance(results, list)
        assert len(results) == 3

    @patch("orchestrator.SolutionExplainer")
    @patch("orchestrator.ProblemGenerator")
    def test_run_each_item_has_problem_and_solution(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_PROBLEMS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_SOLUTION
        mock_exp_class.return_value = mock_exp

        orchestrator = Orchestrator()
        results = orchestrator.run(SAMPLE_TOPIC)

        for item in results:
            assert "problem" in item
            assert "solution" in item

    @patch("orchestrator.SolutionExplainer")
    @patch("orchestrator.ProblemGenerator")
    def test_run_calls_generator_once(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_PROBLEMS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_SOLUTION
        mock_exp_class.return_value = mock_exp

        orchestrator = Orchestrator()
        orchestrator.run(SAMPLE_TOPIC)

        mock_gen.generate.assert_called_once_with(SAMPLE_TOPIC)

    @patch("orchestrator.SolutionExplainer")
    @patch("orchestrator.ProblemGenerator")
    def test_run_calls_explainer_for_each_problem(self, mock_gen_class, mock_exp_class):
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_PROBLEMS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        mock_exp.explain.return_value = SAMPLE_SOLUTION
        mock_exp_class.return_value = mock_exp

        orchestrator = Orchestrator()
        orchestrator.run(SAMPLE_TOPIC)

        # Explainer phải được gọi đúng số lần bằng số bài toán
        assert mock_exp.explain.call_count == len(SAMPLE_PROBLEMS)

    @patch("orchestrator.SolutionExplainer")
    @patch("orchestrator.ProblemGenerator")
    def test_run_graceful_on_explainer_failure(self, mock_gen_class, mock_exp_class):
        """Nếu 1 bài giải thất bại, các bài khác vẫn tiếp tục."""
        mock_gen = MagicMock()
        mock_gen.generate.return_value = SAMPLE_PROBLEMS
        mock_gen_class.return_value = mock_gen

        mock_exp = MagicMock()
        # Bài 1 thất bại, bài 2 và 3 thành công
        mock_exp.explain.side_effect = [
            RuntimeError("Agent 2 lỗi"),
            SAMPLE_SOLUTION,
            SAMPLE_SOLUTION,
        ]
        mock_exp_class.return_value = mock_exp

        orchestrator = Orchestrator()
        results = orchestrator.run(SAMPLE_TOPIC)

        # Vẫn trả về đủ 3 kết quả
        assert len(results) == 3
        # Bài đầu có solution rỗng (graceful fallback)
        assert results[0]["solution"] == {}
        # Bài sau có solution đầy đủ
        assert results[1]["solution"] == SAMPLE_SOLUTION
