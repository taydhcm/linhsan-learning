# Bước 12: UI Tab Toán / Tiếng Việt

## Mục tiêu
Mở rộng giao diện `app.py` từ 1 tab (Toán) thành 2 tab song song: **🧮 Toán** và **📖 Tiếng Việt**.

## File thay đổi
```
source/backend/
└── app.py   ← tái cấu trúc toàn bộ layout
```

## Thay đổi chính

### Imports mới
```python
from vietnamese_topics import VIET_TOPICS
from orchestrator_viet import OrchestratorViet
```

### Tab layout
```python
tab_toan, tab_viet = st.tabs(["🧮 Toán", "📖 Tiếng Việt"])

with tab_toan:
    # ... logic toán (giữ nguyên)

with tab_viet:
    # ... logic tiếng việt (mới)
```

### Session state tách biệt
| Key | Tab | Mô tả |
|---|---|---|
| `toan_results` | Toán | Kết quả bài toán |
| `toan_topic_current` | Toán | Chủ đề đang xem |
| `viet_results` | Tiếng Việt | Kết quả câu hỏi TV |
| `viet_topic_current` | Tiếng Việt | Chủ đề TV đang xem |

### CSS mới
```css
.viet-card   { border-left: 5px solid #43a047; background: #f0fff4; }
.type-badge  { background: #e8f5e9; color: #2e7d32; border-radius: 12px; }
```

### Helper functions
- `render_toan_result(solution)` — render lời giải Toán
- `render_viet_result(explanation)` — render lời giải Tiếng Việt, thêm `type-badge`

## Kết quả
- Người dùng chuyển tab mượt mà, kết quả 2 môn không ảnh hưởng nhau
- Mỗi tab có nút "Bắt đầu học!" và "Tạo lại" riêng
- Tiêu đề trang: `📚 Linhsan Learning — AI Tutor lớp 4`
