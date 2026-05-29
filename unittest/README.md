# Unit Tests

Thư mục chứa tất cả file test, kết quả test và debug output của dự án.

## Cấu trúc

```
unittest/
├── backend/             # Tests cho backend
│   ├── conftest.py      # Pytest fixtures dùng chung
│   └── <module>/        # Test theo từng module
│       └── test_<name>.py
├── frontend/            # Tests cho frontend
│   └── <module>/
│       └── <name>.test.js
├── output/              # Kết quả chạy test (HTML report, coverage…)
│   └── .gitkeep
└── debug/               # Log debug khi chạy test
    └── .gitkeep
```

## Chạy test backend (pytest)

```bash
cd unittest
pytest backend/ -v --html=output/report.html --self-contained-html
```

## Chạy test frontend (jest/vitest)

```bash
cd unittest/frontend
npx vitest run --reporter=verbose
```

## Quy tắc viết test

- Mỗi module phải có ít nhất 1 file test tương ứng
- Coverage tối thiểu: 80%
- Tên test: `test_<hành_động>_<kết_quả_mong_đợi>` (VD: `test_login_returns_token`)
- Không kết nối database thật trong unit test, dùng mock/fixture
