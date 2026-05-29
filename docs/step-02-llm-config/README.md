# Bước 2: Cấu hình LLM API (Groq)

## Mục tiêu
Tích hợp Groq SDK, đọc API key an toàn, cấu hình model.

## LLM Provider: Groq Cloud
- **Tại sao Groq?** Miễn phí, siêu nhanh (LPU chip), quota free đủ dùng 1–2 user
- **Model chính:** `llama-3.3-70b-versatile` — chất lượng cao, tiếng Việt tốt, context 128k
- **Model dự phòng:** `llama-3.1-8b-instant` — nhẹ hơn nếu cần tiết kiệm quota

## Lấy API Key
1. Vào https://console.groq.com
2. Đăng ký bằng Google/GitHub
3. Menu → **API Keys** → **Create API Key**
4. Copy key (dạng `gsk_xxxxxxxxxx`)

## Cấu hình local development
```bash
cd source/backend
cp .env.example .env
# Mở .env, thay gsk_your_api_key_here bằng key thật
```

## Cấu hình Streamlit Cloud (production)
```
App Settings → Secrets → dán:
GROQ_API_KEY = "gsk_your_key_here"
```

## Files thực hiện
| File | Vai trò |
|---|---|
| `source/backend/config.py` | `get_groq_api_key()`, constants model/timeout |
| `source/backend/.env.example` | Template cho local dev |
| `source/backend/.streamlit/secrets.toml.example` | Template cho Streamlit Cloud |

## Thứ tự đọc key (ưu tiên)
1. `st.secrets["GROQ_API_KEY"]` (production)
2. `os.environ["GROQ_API_KEY"]` (local, từ `.env`)
3. Raise `EnvironmentError` nếu không có

## Test
```python
from config import get_groq_api_key
key = get_groq_api_key()
assert key.startswith("gsk_")
```
