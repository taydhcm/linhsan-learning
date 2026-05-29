# Bước 3: topics.py — Danh sách chủ đề

## Mục tiêu
Định nghĩa 7 chủ đề toán lớp 4 với danh sách kiến thức cần bao phủ.

## File: `source/backend/topics.py`

## Cấu trúc mỗi topic
```python
{
    "id": "T1",                     # Định danh
    "name": "Số tự nhiên",          # Tên hiển thị trên UI
    "description": "...",           # Mô tả ngắn
    "knowledge": [                  # List kiến thức Agent 1 phải bao phủ
        "Đọc và viết số tự nhiên đến 1 000 000",
        ...
    ]
}
```

## 7 Chủ đề
| ID | Tên | Số kiến thức |
|---|---|---|
| T1 | Số tự nhiên | 4 |
| T2 | Bốn phép tính số tự nhiên | 5 |
| T3 | Phân số — Khái niệm & tính chất | 5 |
| T4 | Bốn phép tính phân số | 5 |
| T5 | Hình học | 5 |
| T6 | Đo lường | 4 |
| T7 | Toán có lời văn | 4 |

## Test
```python
from topics import TOPICS, get_topic_by_id
assert len(TOPICS) == 7
t1 = get_topic_by_id("T1")
assert t1["name"] == "Số tự nhiên"
assert len(t1["knowledge"]) >= 3
```
