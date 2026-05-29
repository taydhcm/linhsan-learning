# PROJECT_ARCHITECTURE_TEMPLATE.md

> **Mục đích:** File này là template kiến trúc dự án. Khi khởi tạo dự án mới, chỉ cần cung cấp file này cho Claude — AI sẽ tự động tạo toàn bộ cấu trúc thư mục và file khung giống dự án hiện tại.

---

## Cách dùng template này

1. Copy toàn bộ file này vào workspace mới
2. Nói với Claude: *"Hãy tạo một dự án mới theo file PROJECT_ARCHITECTURE_TEMPLATE.md này"*
3. Claude sẽ scaffold toàn bộ cấu trúc, bao gồm: thư mục, file cấu hình, README và file mẫu

---

## Cây thư mục chuẩn

```
<project-root>/
│
├── .claude/
│   └── settings.local.json          # Cấu hình Claude agent cho dự án
│
├── access/                          # Tài nguyên dự án (hình ảnh, file, dữ liệu mẫu…)
│   └── .gitkeep
│
├── docs/                            # Tài liệu mô tả, hướng dẫn, TODO list
│   ├── overview.html                # Trang HTML tổng quan + bảng TODO
│   └── guide.md                     # Hướng dẫn phát triển module
│
├── source/                          # Source code chính
│   ├── backend/                     # Server-side code
│   │   └── README.md
│   └── frontend/                    # Client-side code
│       └── README.md
│
├── unittest/                        # Tests, output, debug
│   ├── output/                      # Test reports (HTML, coverage)
│   │   └── .gitkeep
│   ├── debug/                       # Debug logs
│   │   └── .gitkeep
│   └── README.md
│
├── CLAUDE.md                        # Tổng quan dự án cho Claude AI
├── PROJECT_ARCHITECTURE_TEMPLATE.md # File này — template để tái tạo cấu trúc
└── PROJECT_REQUIREMENTS.md          # Yêu cầu nghiệp vụ chi tiết
```

---

## Nội dung từng file/thư mục

### `.claude/settings.local.json`
Cấu hình Claude agent: model, context include/exclude, project rules.

**Template:**
```json
{
  "agent": {
    "name": "<project-name>-agent",
    "version": "1.0.0",
    "description": "Claude agent configuration for <project-name>"
  },
  "claude": {
    "model": "claude-sonnet-4-5",
    "max_tokens": 8192,
    "temperature": 0.7
  },
  "project": {
    "name": "<project-name>",
    "root": ".",
    "language": "<primary-language>"
  },
  "context": {
    "include": [
      "CLAUDE.md",
      "PROJECT_REQUIREMENTS.md",
      "PROJECT_ARCHITECTURE_TEMPLATE.md",
      "docs/**/*.md",
      "source/**/*"
    ],
    "exclude": [
      "unittest/output/**",
      "**/__pycache__/**",
      "**/node_modules/**",
      "**/.git/**"
    ]
  },
  "rules": [
    "Always follow the architecture defined in PROJECT_ARCHITECTURE_TEMPLATE.md",
    "Check PROJECT_REQUIREMENTS.md before implementing any feature",
    "Write unit tests for every new module in the unittest/ folder"
  ]
}
```

---

### `docs/overview.html`
Trang HTML tổng quan: mô tả ngắn dự án, bảng TODO với trạng thái từng module (TODO / In Progress / Done), hướng dẫn AI thực hiện module, links tới các file quan trọng.

---

### `docs/guide.md`
Markdown hướng dẫn:
- Quy trình implement module mới (bước 1→5)
- Quy ước đặt tên (file, class, function, API endpoint)
- Cấu trúc chuẩn một module backend và frontend
- Checklist trước khi hoàn thành module

---

### `source/backend/`
Chứa toàn bộ server-side code. Cấu trúc nội bộ phụ thuộc framework:

| Framework | Entry point       | Module pattern                   |
|-----------|-------------------|----------------------------------|
| FastAPI   | `app/main.py`     | `app/<module>/{models,routes,service,repository}.py` |
| Flask     | `app/__init__.py` | `app/<module>/views.py`          |
| Django    | `manage.py`       | `<module>/views.py`, `models.py` |

---

### `source/frontend/`
Chứa toàn bộ client-side code. Cấu trúc nội bộ phụ thuộc framework:

| Framework | Entry point     | Component pattern                |
|-----------|-----------------|----------------------------------|
| Vue 3     | `src/main.js`   | `src/components/<Module>.vue`    |
| React     | `src/index.jsx` | `src/components/<Module>.jsx`    |
| Vanilla   | `index.html`    | `src/pages/<module>/index.html`  |

---

### `unittest/`
```
unittest/
├── backend/
│   ├── conftest.py        # Pytest fixtures
│   └── <module>/
│       └── test_<name>.py
├── frontend/
│   └── <module>/
│       └── <name>.test.js
├── output/                # Reports (auto-generated, gitignored contents)
└── debug/                 # Debug logs (auto-generated, gitignored contents)
```

---

### `CLAUDE.md`
Bắt buộc chứa:
1. **Dự án là gì** — mô tả ngắn gọn mục đích, đối tượng sử dụng
2. **Chúng ta cần làm gì** — danh sách mục tiêu
3. **Thiết kế hệ thống** — stack công nghệ, sơ đồ kiến trúc
4. **Các chức năng chính** — bảng module + mô tả
5. **Testing** — công cụ, cách chạy, yêu cầu coverage
6. **Deploy** — môi trường dev/prod, checklist
7. **Quy tắc làm việc với Claude** — ràng buộc quan trọng

---

### `PROJECT_REQUIREMENTS.md`
Bắt buộc chứa:
1. **Thông tin dự án** — tên, mục tiêu, đối tượng, phạm vi
2. **Yêu cầu chức năng** — danh sách use case / user story theo module
3. **Yêu cầu phi chức năng** — hiệu năng, bảo mật, khả năng mở rộng
4. **Ràng buộc kỹ thuật** — ngôn ngữ, framework, database bắt buộc
5. **Tiêu chí nghiệm thu** — định nghĩa "done" cho từng module

---

## Hướng dẫn Claude tạo dự án mới từ template

Khi người dùng yêu cầu tạo dự án mới với file này, Claude cần:

1. Hỏi tên dự án, ngôn ngữ/framework chính nếu chưa có
2. Tạo toàn bộ cây thư mục như mô tả ở trên
3. Điền `<project-name>` và `<primary-language>` vào `settings.local.json`
4. Tạo `CLAUDE.md` với sections đầy đủ, placeholder nội dung
5. Tạo `PROJECT_REQUIREMENTS.md` với sections đầy đủ, placeholder
6. Tạo `docs/overview.html` với bảng TODO trống
7. Tạo `docs/guide.md` với quy ước phù hợp framework đã chọn
8. Tạo `source/backend/README.md` và `source/frontend/README.md`
9. Tạo `unittest/README.md`, `unittest/output/.gitkeep`, `unittest/debug/.gitkeep`
