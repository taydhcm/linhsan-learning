"""
conftest.py — Pytest fixtures và path setup cho unittest/backend/.

Tự động thêm source/backend vào sys.path và set GROQ_API_KEY giả
để các test không cần file .env thật và không tốn API credit.
"""

import sys
import os

# Đặt fake API key trước khi import bất kỳ module nào dùng config
os.environ.setdefault("GROQ_API_KEY", "gsk_test_fake_key_for_unit_testing")

# Thêm source/backend vào Python path
_BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "source", "backend")
)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)
