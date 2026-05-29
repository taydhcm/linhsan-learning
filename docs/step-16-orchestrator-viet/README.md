# Bước 16: Orchestrator Tiếng Việt

## Mục tiêu
Pipeline kết nối `VietQuestionGenerator` (Agent 1) → `VietAnswerExplainer` (Agent 2), xử lý từng câu hỏi tuần tự với retry và fallback.

## File tạo mới
```
source/backend/
└── orchestrator_viet.py   ← MỚI
```

## Class `OrchestratorViet`

```python
class OrchestratorViet:
    def __init__(self, api_key: str | None = None): ...
    def run(self, topic: dict) -> list[dict]: ...
```

### Luồng xử lý
```
topic (dict)
    │
    ▼
VietQuestionGenerator.generate(topic)
    → list[question_dict]  (6 câu hỏi)
    │
    ▼ (for each question)
VietAnswerExplainer.explain(question)
    → explanation_dict
    │
    ▼
[{ question, explanation }, ...]  ← kết quả trả về app.py
```

### Output format
```python
[
    {
        "question":    { id, level, type, question, hint },
        "explanation": { question_id, read_question, thinking_direction,
                         steps, answer, explanation, skill_note }
    },
    ...
]
```

## Xử lý lỗi & Fallback

```python
try:
    explanation = self.explainer.explain(question)
except Exception as e:
    explanation = {}   # fallback: UI sẽ hiện warning thay vì crash
```

Tương tự `orchestrator.py` cho Toán — nếu Agent 2 lỗi ở 1 câu, các câu còn lại vẫn hiển thị.

## Sử dụng trong app.py

```python
from orchestrator_viet import OrchestratorViet

results = OrchestratorViet().run(selected_viet_topic)
# → list[{question, explanation}]
```

## So sánh với Orchestrator Toán
| Toán (`orchestrator.py`) | Tiếng Việt (`orchestrator_viet.py`) |
|---|---|
| `ProblemGenerator` | `VietQuestionGenerator` |
| `SolutionExplainer` | `VietAnswerExplainer` |
| key `"problem"` | key `"question"` |
| key `"solution"` | key `"explanation"` |
