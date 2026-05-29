# Bước 13: vietnamese_topics.py

## Mục tiêu
Định nghĩa 7 chủ đề Tiếng Việt lớp 4 với danh sách kỹ năng cần bao phủ cho mỗi chủ đề — tương tự `topics.py` cho Toán.

## File tạo mới
```
source/backend/
└── vietnamese_topics.py   ← MỚI
```

## Cấu trúc dữ liệu

```python
VIET_TOPICS: list[dict] = [
    {
        "id": "V1",
        "name": "Tập đọc — Đọc hiểu",
        "description": "...",
        "skills": [
            "Tìm ý chính của đoạn văn/bài văn",
            "Nhận biết nhân vật chính và đặc điểm",
            ...
        ]
    },
    ...
]
```

## 7 Chủ đề

| ID | Tên chủ đề | Số kỹ năng |
|----|-----------|-----------|
| V1 | Tập đọc — Đọc hiểu | 5 kỹ năng |
| V2 | Từ loại | 5 kỹ năng |
| V3 | Cấu tạo từ | 5 kỹ năng |
| V4 | Cấu tạo câu | 5 kỹ năng |
| V5 | Chính tả | 5 kỹ năng |
| V6 | Văn kể chuyện | 5 kỹ năng |
| V7 | Văn miêu tả | 5 kỹ năng |

## Helper function

```python
def get_viet_topic_by_id(topic_id: str) -> dict | None:
    """Trả về topic dict theo ID (V1–V7), None nếu không tìm thấy."""
    return next((t for t in VIET_TOPICS if t["id"] == topic_id), None)
```

## Sử dụng trong app.py

```python
from vietnamese_topics import VIET_TOPICS

viet_topic_map = {t["name"]: t for t in VIET_TOPICS}
selected = st.selectbox("Chọn chủ đề:", list(viet_topic_map.keys()))
topic = viet_topic_map[selected]
```
