# Bước 7: Orchestrator / Pipeline

## Mục tiêu
Kết nối Agent 1 và Agent 2 thành pipeline hoàn chỉnh.

## File: `source/backend/orchestrator.py`

## Luồng xử lý
```
topic (dict)
    │
    ▼
ProblemGenerator.generate(topic)
    │  → list[dict] (6 bài toán)
    │
    ├── problem[0] ──▶ SolutionExplainer.explain(p) → solution[0]
    ├── problem[1] ──▶ SolutionExplainer.explain(p) → solution[1]
    │   ...
    └── problem[5] ──▶ SolutionExplainer.explain(p) → solution[5]
    │
    ▼
list[{"problem": {...}, "solution": {...}}]
```

## Xử lý lỗi
- Nếu `SolutionExplainer` thất bại cho 1 bài → trả `solution = {}` (graceful fallback)
- Các bài còn lại vẫn tiếp tục xử lý

## Test
```bash
cd unittest
pytest backend/test_orchestrator.py -v
```
