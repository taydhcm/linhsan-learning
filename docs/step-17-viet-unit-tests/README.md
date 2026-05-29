# Bước 17: Unit Tests — Module Tiếng Việt

## Mục tiêu
Test toàn bộ agents và orchestrator Tiếng Việt với mock LLM — không tốn API credit.

## Cấu trúc test
```
unittest/backend/
├── test_viet_question_generator.py   ← MỚI
├── test_viet_answer_explainer.py     ← MỚI
└── test_orchestrator_viet.py         ← MỚI
```

## Chạy test
```bash
# Từ thư mục gốc dự án
cd unittest
pytest backend/test_viet_question_generator.py -v
pytest backend/test_viet_answer_explainer.py -v
pytest backend/test_orchestrator_viet.py -v

# Tất cả cùng lúc
pytest backend/ -v
```

## Chiến lược mock — VietQuestionGenerator
```python
@patch("agents.viet_question_generator.Groq")
def test_generate_returns_6_questions(mock_groq_class):
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps([
        {"id": "q1", "level": "nhận_biết",  "type": "trắc_nghiệm",    "question": "...", "hint": "..."},
        {"id": "q2", "level": "nhận_biết",  "type": "điền_chỗ_trống", "question": "...", "hint": "..."},
        {"id": "q3", "level": "thông_hiểu", "type": "trắc_nghiệm",    "question": "...", "hint": "..."},
        {"id": "q4", "level": "thông_hiểu", "type": "tự_luận",         "question": "...", "hint": "..."},
        {"id": "q5", "level": "vận_dụng",   "type": "tự_luận",         "question": "...", "hint": "..."},
        {"id": "q6", "level": "vận_dụng",   "type": "tự_luận",         "question": "...", "hint": "..."},
    ])

    from agents.viet_question_generator import VietQuestionGenerator
    gen = VietQuestionGenerator(api_key="test-key")
    topic = {"id": "V2", "name": "Từ loại", "skills": ["Nhận biết danh từ"]}
    questions = gen.generate(topic)

    assert len(questions) == 6
    levels = {q["level"] for q in questions}
    assert levels == {"nhận_biết", "thông_hiểu", "vận_dụng"}
```

## Test cases — VietQuestionGenerator
| Test | Mô tả |
|---|---|
| `test_generate_returns_6_questions` | Output đủ 6 câu hỏi |
| `test_generate_has_all_3_levels` | Có đủ 3 level |
| `test_generate_valid_types` | type phải là 1 trong 3 giá trị hợp lệ |
| `test_generate_all_fields_present` | Mỗi câu có id, level, type, question, hint |
| `test_generate_json_parse_error_fallback` | LLM trả về JSON lỗi → xử lý gracefully |

## Test cases — VietAnswerExplainer
| Test | Mô tả |
|---|---|
| `test_explain_returns_all_fields` | Output có đủ 6 fields |
| `test_explain_steps_is_list` | `steps` là list, không rỗng |
| `test_explain_answer_not_empty` | `answer` không được rỗng |
| `test_explain_skill_note_present` | `skill_note` không được rỗng |

## Test cases — OrchestratorViet
| Test | Mô tả |
|---|---|
| `test_run_returns_list` | Output là list |
| `test_run_each_item_has_question_and_explanation` | Mỗi item có 2 keys |
| `test_run_explainer_failure_graceful` | Nếu explainer lỗi, item vẫn có question, explanation = {} |

## Coverage targets
| Module | Test cases | Target coverage |
|---|---|---|
| viet_question_generator.py | 5 | ≥ 85% |
| viet_answer_explainer.py | 4 | ≥ 85% |
| orchestrator_viet.py | 3 | ≥ 80% |

## Kết quả mong đợi
```
========================= 12+ passed in x.xxs ==========================
```
