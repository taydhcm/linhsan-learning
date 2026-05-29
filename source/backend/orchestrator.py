"""
orchestrator.py — Pipeline kết nối Agent 1 và Agent 2.

Luồng:
  1. Nhận topic từ UI
  2. Gọi Agent 1 → nhận list bài toán (JSON)
  3. Với mỗi bài toán, gọi Agent 2 → nhận lời giải (JSON)
  4. Trả về list cặp {problem, solution}
"""

from agents.problem_generator import ProblemGenerator
from agents.solution_explainer import SolutionExplainer


class Orchestrator:
    """Điều phối pipeline: sinh bài toán → giải thích từng bài."""

    def __init__(self):
        self.generator = ProblemGenerator()
        self.explainer = SolutionExplainer()

    def run(self, topic: dict) -> list[dict]:
        """
        Chạy toàn bộ pipeline cho một chủ đề.

        Args:
            topic: dict chứa thông tin chủ đề (id, name, knowledge...)

        Returns:
            list of dict: [{"problem": {...}, "solution": {...}}, ...]
        """
        problems = self.generator.generate(topic)
        results = []

        for problem in problems:
            try:
                solution = self.explainer.explain(problem)
            except RuntimeError:
                # Graceful fallback: nếu 1 bài giải thất bại, vẫn tiếp tục các bài còn lại
                solution = {}

            results.append({"problem": problem, "solution": solution})

        return results
