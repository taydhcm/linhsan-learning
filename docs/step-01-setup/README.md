# Bước 1: Setup Project Streamlit

## Mục tiêu
Tạo cấu trúc thư mục chuẩn và các file khung cho Streamlit app.

## Files đã tạo / cập nhật
| File | Mô tả |
|---|---|
| `source/backend/app.py` | Entry point Streamlit |
| `source/backend/requirements.txt` | Python dependencies |
| `source/backend/.env.example` | Template biến môi trường |
| `source/backend/.streamlit/secrets.toml.example` | Template Streamlit secrets |
| `.gitignore` | Bảo vệ .env và secrets khỏi Git |

## Cấu trúc thư mục backend
```
source/backend/
├── app.py
├── config.py
├── topics.py
├── utils.py
├── orchestrator.py
├── agents/
│   ├── __init__.py
│   ├── problem_generator.py
│   └── solution_explainer.py
├── prompts/
│   ├── problem_generator.j2
│   └── solution_explainer.j2
├── requirements.txt
├── .env.example
└── .streamlit/
    └── secrets.toml.example
```

## Test thủ công
```bash
cd source/backend
pip install -r requirements.txt
streamlit run app.py
```

## Kết quả mong đợi
- App khởi động tại http://localhost:8501
- Nếu thiếu GROQ_API_KEY, app hiển thị thông báo lỗi thân thiện
