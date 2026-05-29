"""
config.py — Cấu hình toàn cục cho linhsan-learning app.

Thứ tự đọc API key:
  1. st.secrets["GROQ_API_KEY"]  (Streamlit Cloud production)
  2. os.environ["GROQ_API_KEY"]  (local .env qua python-dotenv)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env từ cùng thư mục với config.py — hoạt động dù chạy từ bất kỳ đâu
_ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE)

try:
    import streamlit as st
    _secrets_available = True
except ImportError:
    _secrets_available = False


def get_groq_api_key() -> str:
    """Đọc GROQ_API_KEY từ st.secrets (prod) hoặc os.environ (dev)."""
    # 1. Thử từ Streamlit secrets (production / Streamlit Cloud)
    if _secrets_available:
        try:
            key = st.secrets.get("GROQ_API_KEY", "")
            if key:
                return key
        except Exception:
            pass

    # 2. Fallback: biến môi trường (local dev với .env)
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key

    raise EnvironmentError(
        "GROQ_API_KEY chưa được cấu hình.\n"
        "- Local: thêm GROQ_API_KEY=gsk_xxx vào file .env\n"
        "- Streamlit Cloud: thêm vào Settings → Secrets"
    )


# ── LLM settings ──────────────────────────────────────────────────────────────
LLM_MODEL_PRIMARY = "llama-3.3-70b-versatile"   # Nhanh, chất lượng cao
LLM_MODEL_FALLBACK = "llama-3.1-8b-instant"     # Nhẹ hơn, dùng khi quota hết

LLM_MAX_TOKENS = 4096        # Đủ cho bài giải chi tiết
LLM_TEMPERATURE = 0.7        # Sáng tạo vừa phải — không quá ngẫu nhiên
LLM_TIMEOUT_SECONDS = 60     # Timeout mỗi LLM call
LLM_MAX_RETRIES = 3          # Số lần retry khi JSON parse thất bại

# ── Agent settings ─────────────────────────────────────────────────────────────
PROBLEMS_PER_SESSION = 6     # Số bài toán Agent 1 sinh ra mỗi lần
MIN_PROBLEMS_PER_LEVEL = 1   # Mỗi level (biết/hiểu/vận_dụng) ít nhất 1 bài
