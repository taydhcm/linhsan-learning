# Frontend Source Code

Thư mục chứa toàn bộ source code phía client (UI, components, API calls).

## Cấu trúc gợi ý

```
frontend/
├── public/              # Static files (favicon, robots.txt…)
├── src/
│   ├── assets/          # Hình ảnh, fonts, styles toàn cục
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page-level components / views
│   ├── services/        # Giao tiếp API (axios / fetch)
│   ├── store/           # State management (Redux / Pinia / Zustand)
│   ├── router/          # Routing config
│   ├── utils/           # Helper functions
│   └── main.js          # Entry point
├── package.json
├── .env.example         # Mẫu biến môi trường
└── README.md
```

## Khởi động (Development)

```bash
cd source/frontend
npm install
npm run dev
```
