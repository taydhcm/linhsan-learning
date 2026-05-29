# Bước 5: Agent 1 — Problem Generator

## Mục tiêu
Sinh 6 bài toán theo chủ đề, bao phủ đủ 3 cấp độ tư duy Bloom.

## File: `source/backend/agents/problem_generator.py`
## Prompt: `source/backend/prompts/problem_generator.j2`

## Cấp độ bài toán
| Cấp độ | Mô tả | Số bài tối thiểu |
|---|---|---|
| `biết` | Nhận biết, tính trực tiếp theo công thức | 2 |
| `hiểu` | Giải thích, chuyển đổi, so sánh | 2 |
| `vận_dụng` | Lời văn, tình huống thực tế, nhiều bước | 2 |

## Output schema
```json
[
  {
    "id": 1,
    "level": "biết | hiểu | vận_dụng",
    "question": "Nội dung bài toán đầy đủ...",
    "hint": "Gợi ý không tiết lộ đáp án..."
  }
]
```

## Xử lý lỗi
- Retry tối đa `LLM_MAX_RETRIES` lần nếu JSON parse thất bại
- Raise `RuntimeError` sau khi hết retry

## Test
```bash
cd unittest
pytest backend/test_problem_generator.py -v
```
