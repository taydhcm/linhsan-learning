# Bước 14: Agent 1 — Question Generator (Tiếng Việt)

## Mục tiêu
Sinh 6 câu hỏi ôn tập Tiếng Việt theo chủ đề, bao phủ đủ 3 cấp độ tư duy (Nhận biết / Thông hiểu / Vận dụng) và 3 dạng câu hỏi.

## File tạo mới
```
source/backend/
├── agents/viet_question_generator.py   ← MỚI
└── prompts/viet_question_generator.j2  ← MỚI
```

## Class `VietQuestionGenerator`

```python
class VietQuestionGenerator:
    def __init__(self, api_key: str): ...
    def generate(self, topic: dict, num_questions: int = 6) -> list[dict]: ...
```

### Output JSON schema
```json
[
  {
    "id": "q1",
    "level": "nhận_biết",
    "type": "trắc_nghiệm",
    "question": "Câu hỏi đầy đủ...",
    "hint": "Gợi ý ngắn..."
  }
]
```

### Giá trị hợp lệ
| Field | Giá trị |
|---|---|
| `level` | `nhận_biết` \| `thông_hiểu` \| `vận_dụng` |
| `type` | `trắc_nghiệm` \| `tự_luận` \| `điền_chỗ_trống` |

## Prompt template (viet_question_generator.j2)

```jinja
Bạn là giáo viên Tiếng Việt lớp 4 tại Việt Nam.
Hãy tạo {{ num_questions }} câu hỏi ôn tập chủ đề "{{ topic.name }}".

Kỹ năng cần bao phủ: {{ topic.skills }}

Yêu cầu:
- 2 câu "nhận_biết" (trắc_nghiệm hoặc điền_chỗ_trống)
- 2 câu "thông_hiểu" (trắc_nghiệm hoặc tự_luận)
- 2 câu "vận_dụng" (tự_luận)
...
Output: JSON array [{ id, level, type, question, hint }]
```

## Chiến lược phân bổ câu hỏi
| Cấp độ | Số câu | Dạng ưu tiên |
|---|---|---|
| nhận_biết (2 câu) | Nhận ra, chọn đúng/sai | trắc_nghiệm, điền_chỗ_trống |
| thông_hiểu (2 câu) | Phân tích, giải thích | trắc_nghiệm, tự_luận |
| vận_dụng (2 câu) | Đặt câu, viết đoạn | tự_luận |

## Xử lý lỗi
```python
try:
    questions = json.loads(raw_content)
except json.JSONDecodeError:
    # Thử extract JSON từ markdown block
    questions = parse_json_from_llm_output(raw_content)
```
