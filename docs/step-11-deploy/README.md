# Bước 11: Deploy lên Streamlit Community Cloud

## Điều kiện trước khi deploy
- [ ] Có tài khoản GitHub (repo public hoặc private)
- [ ] Có Groq API Key (lấy tại https://console.groq.com)
- [ ] Tất cả test pass (`pytest backend/ -v`)
- [ ] Không có `print()` debug còn sót trong code

## Bước 1: Push lên GitHub
```bash
git init
git add .
git commit -m "feat: initial release — AI Math Tutor lớp 4"
git remote add origin https://github.com/<username>/linhsan-learning.git
git push -u origin main
```

## Bước 2: Deploy trên Streamlit Cloud
1. Vào https://share.streamlit.io
2. **New app** → chọn repo → branch: `main`
3. **Main file path:** `source/backend/app.py`
4. Click **Deploy**

## Bước 3: Cấu hình Secrets
1. App settings → **Secrets**
2. Dán nội dung:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
3. Save → App tự động restart

## Checklist deploy
- [ ] `GROQ_API_KEY` đã set trong Streamlit Secrets
- [ ] `requirements.txt` đầy đủ, pin version
- [ ] App load không lỗi tại URL streamlit.app
- [ ] Chọn chủ đề và nhấn "Bắt đầu học!" → kết quả hiện đúng
- [ ] Nút "Tạo lại" hoạt động
- [ ] Lỗi LLM được hiển thị thông báo thân thiện

## URL sau khi deploy
`https://<app-name>.streamlit.app`
