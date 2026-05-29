# Bước 6: Agent 2 — Solution Explainer

## Mục tiêu
Giải và giải thích từng bài toán theo cách trẻ em 5–6 tuổi có thể hiểu được.

## File: `source/backend/agents/solution_explainer.py`
## Prompt: `source/backend/prompts/solution_explainer.j2`

## Nguyên tắc giải thích
1. Ngôn ngữ đơn giản, như đang nói chuyện với em bé
2. Dùng hình ảnh quen thuộc: kẹo, bánh, tiền xu, táo...
3. Giải thích TẠI SAO, không chỉ CÁCH làm
4. Mỗi bước ngắn, rõ ràng

## Output schema
```json
{
  "problem_id": 1,
  "read_problem": "Tóm tắt đề bài đơn giản...",
  "thinking_direction": "Chúng mình sẽ làm thế này nhé...",
  "steps": ["Bước 1: ...", "Bước 2: ..."],
  "answer": "Vậy đáp án là...",
  "explanation": "Giải thích bằng hình ảnh thực tế...",
  "skill_note": "Kỹ năng tư duy học được..."
}
```

## Fields bắt buộc
Tất cả 7 fields đều phải có. Nếu thiếu → retry.

## Test
```bash
cd unittest
pytest backend/test_solution_explainer.py -v
```
