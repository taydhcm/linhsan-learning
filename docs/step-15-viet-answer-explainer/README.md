# Bước 15: Agent 2 — Answer Explainer (Tiếng Việt)

## Mục tiêu
Nhận từng câu hỏi Tiếng Việt từ Agent 1 → giải thích đáp án bằng ngôn ngữ cực kỳ đơn giản, như đang nói chuyện với bé 5–6 tuổi, đồng thời định hình kỹ năng TV lâu dài.

## File tạo mới
```
source/backend/
├── agents/viet_answer_explainer.py   ← MỚI
└── prompts/viet_answer_explainer.j2  ← MỚI
```

## Class `VietAnswerExplainer`

```python
class VietAnswerExplainer:
    def __init__(self, api_key: str): ...
    def explain(self, question: dict) -> dict: ...
```

### Output JSON schema
```json
{
  "question_id": "q1",
  "read_question":       "Câu hỏi này hỏi mình...",
  "thinking_direction":  "Chúng mình sẽ...",
  "steps": [
    "Bước 1: ...",
    "Bước 2: ..."
  ],
  "answer":      "Đáp án đúng là...",
  "explanation": "Giải thích hình ảnh dễ hiểu...",
  "skill_note":  "Kỹ năng Tiếng Việt học được: ..."
}
```

## Prompt template (viet_answer_explainer.j2)

```jinja
Bạn là cô giáo Tiếng Việt thân thiện, giải thích như nói chuyện với bé 5 tuổi.
Câu hỏi ({{ question.level }} — {{ question.type }}):
{{ question.question }}

Hãy giải thích đáp án đầy đủ theo format JSON:
{ read_question, thinking_direction, steps[], answer, explanation, skill_note }
```

## Nguyên tắc giải thích Tiếng Việt
1. **Ví dụ từ cuộc sống**: trường học, gia đình, đồ chơi quen thuộc với trẻ
2. **Giải thích "tại sao"**: không chỉ cho đáp án mà còn lý do
3. **So sánh đúng/sai**: đặt 2 trường hợp để bé dễ nhận ra
4. **skill_note** phải gắn với kỹ năng TV thực tế (từ loại, cấu tạo câu, v.v.)

## Sự khác biệt so với Agent 2 Toán
| Toán | Tiếng Việt |
|---|---|
| `read_problem` | `read_question` |
| Dùng hình ảnh: bánh pizza, kẹo | Dùng hình ảnh: câu chuyện, đồ chơi |
| `skill_note` = kỹ năng tư duy | `skill_note` = kỹ năng TV (ngữ pháp, chính tả) |
