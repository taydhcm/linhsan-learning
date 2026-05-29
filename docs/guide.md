# Hướng dẫn phát triển module

Tài liệu này hướng dẫn AI (Claude) và lập trình viên cách triển khai từng module trong dự án **linhsan-learning**.

---

## Quy trình thực hiện một module mới

1. **Đọc yêu cầu** từ `PROJECT_REQUIREMENTS.md`
2. **Xác định vị trí code** theo `PROJECT_ARCHITECTURE_TEMPLATE.md`
3. **Triển khai backend** tại `source/backend/<module_name>/`
4. **Triển khai frontend** tại `source/frontend/<module_name>/`
5. **Viết unit test** tại `unittest/<module_name>/`
6. **Cập nhật docs** tại `docs/` nếu cần

---

## Quy ước đặt tên

| Loại          | Quy ước             | Ví dụ                  |
|---------------|---------------------|------------------------|
| File Python   | snake_case          | `user_service.py`      |
| Class         | PascalCase          | `UserService`          |
| Function      | snake_case          | `get_user_by_id()`     |
| Variable      | snake_case          | `user_list`            |
| Constant      | UPPER_SNAKE_CASE    | `MAX_RETRY_COUNT`      |
| API endpoint  | kebab-case          | `/api/user-profile`    |
| Component Vue/React | PascalCase   | `UserProfile.vue`      |

---

## Cấu trúc một module backend (Python)

```
source/backend/<module_name>/
├── __init__.py
├── models.py        # Data models / ORM
├── schemas.py       # Pydantic schemas (nếu dùng FastAPI)
├── routes.py        # API routes / endpoints
├── service.py       # Business logic
└── repository.py   # Database access layer
```

---

## Cấu trúc một module frontend

```
source/frontend/<module_name>/
├── index.html       # Entry point (nếu vanilla)
├── components/      # UI components
├── services/        # API calls
└── styles/          # CSS/SCSS
```

---

## Checklist trước khi hoàn thành module

- [ ] Code đúng vị trí theo kiến trúc
- [ ] Có unit test với coverage >= 80%
- [ ] API được document (docstring hoặc OpenAPI)
- [ ] Không có secret/credential hard-coded
- [ ] Đã kiểm tra OWASP Top 10 (input validation, auth, injection)
- [ ] Cập nhật `TODO` trong `docs/overview.html`
