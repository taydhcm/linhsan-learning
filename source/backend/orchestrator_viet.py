"""
orchestrator_viet.py — Pipeline Tiếng Việt: kết nối Agent 1 TV và Agent 2 TV.

Luồng:
  1. Nhận topic TV từ UI
  2. Gọi Agent 1 (VietQuestionGenerator) → nhận list câu hỏi (JSON)
  3. Với mỗi câu hỏi, gọi Agent 2 (VietAnswerExplainer) → nhận lời giải thích (JSON)
  4. Trả về list cặp {question, explanation}
"""

from agents.viet_question_generator import VietQuestionGenerator
from agents.viet_answer_explainer import VietAnswerExplainer


class OrchestratorViet:
    """Điều phối pipeline Tiếng Việt: sinh câu hỏi → giải thích từng câu."""

    def __init__(self):
        self.generator = VietQuestionGenerator()
        self.explainer = VietAnswerExplainer()

    def run(self, topic: dict) -> list[dict]:
        """
        Chạy toàn bộ pipeline TV cho một chủ đề.

        Args:
            topic: dict chứa thông tin chủ đề TV (id, name, skills...)

        Returns:
            list of dict: [{"question": {...}, "explanation": {...}}, ...]
        """
        questions = self.generator.generate(topic)
        results = []

        for question in questions:
            try:
                explanation = self.explainer.explain(question)
            except RuntimeError:
                # Graceful fallback: nếu 1 câu giải thất bại, vẫn tiếp tục các câu còn lại
                explanation = {}

            results.append({"question": question, "explanation": explanation})

        return results
