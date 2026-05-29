# Backend Source Code

Thư mục chứa toàn bộ source code phía server (API, business logic, database).

## Cấu trúc gợi ý

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point (FastAPI / Flask app)
│   ├── config.py        # Cấu hình ứng dụng, đọc từ .env
│   ├── dependencies.py  # Dependency injection
│   ├── database.py      # Kết nối database
│   └── <module>/        # Mỗi feature là 1 thư mục riêng
│       ├── __init__.py
│       ├── models.py
│       ├── schemas.py
│       ├── routes.py
│       ├── service.py
│       └── repository.py
├── migrations/          # Database migration scripts
├── requirements.txt     # Python dependencies
├── .env.example         # Mẫu biến môi trường (KHÔNG chứa secret thật)
└── README.md
```

## Khởi động (Development)

```bash
cd source/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
