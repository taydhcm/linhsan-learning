# Bước 10: Unit Tests

## Mục tiêu
Test toàn bộ agents và orchestrator với mock LLM — không tốn API credit.

## Cấu trúc test
```
unittest/backend/
├── conftest.py                    # Path setup + fake API key
├── test_utils.py                  # Test JSON parsing helpers
├── test_problem_generator.py      # Test Agent 1
├── test_solution_explainer.py     # Test Agent 2
└── test_orchestrator.py           # Test pipeline end-to-end
```

## Chạy test
```bash
# Từ thư mục gốc dự án
cd unittest
pytest backend/ -v

# Với HTML report
pytest backend/ -v --html=output/report.html --self-contained-html
```

## Chiến lược mock
```python
@patch("agents.problem_generator.Groq")
def test_generate(mock_groq_class):
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(...)
    ...
```

## Coverage targets
| Module | Test cases | Coverage |
|---|---|---|
| utils.py | 8 | ~100% |
| problem_generator.py | 6 | ~90% |
| solution_explainer.py | 7 | ~90% |
| orchestrator.py | 5 | ~85% |

## Kết quả mong đợi
```
========================= 26 passed in x.xxs ==========================
```
