# CLAUDE.md — Tổng quan dự án linhsan-learning

> File này là nguồn thông tin chính cho Claude AI khi làm việc với dự án này.  
> Đọc kỹ toàn bộ trước khi thực hiện bất kỳ thay đổi nào.

---

## 1. Dự án là gì?

**linhsan-learning** là một ứng dụng web học toán thông minh dành cho học sinh lớp 4 Việt Nam (9–10 tuổi), được triển khai trên **Streamlit Community Cloud**. Hệ thống sử dụng **2 AI Agent** phối hợp để:

1. **Agent tạo bài toán** — Sinh các bài toán phù hợp với chủ đề người dùng chọn, đảm bảo bao phủ 3 cấp độ tư duy: Biết → Hiểu → Vận dụng.
2. **Agent giải & giải thích** — Giải từng bài toán theo phong cách giải thích cực kỳ đơn giản, dễ hiểu như đang nói chuyện với một bạn nhỏ 5–6 tuổi; đồng thời định hình tư duy và kỹ năng giải toán cho trẻ.

Quy mô: **nhỏ gọn, 1–2 người dùng**, không cần database, không cần auth phức tạp.

---

## 2. Chúng ta cần làm gì?

### Danh sách TODO để hiện thực hóa ý tưởng

| # | Hạng mục | Mô tả | Ưu tiên |
|---|---|---|---|
| 1 | **Setup project Streamlit** | Tạo `app.py`, cấu trúc thư mục, `requirements.txt` | 🔴 P0 |
| 2 | **Cấu hình LLM API** | Tích hợp Claude API (Anthropic) hoặc OpenAI, đọc key từ `st.secrets` / `.env` | 🔴 P0 |
| 3 | **UI chọn chủ đề** | Dropdown/card chọn 1 trong 7 chủ đề toán lớp 4 | 🔴 P0 |
| 4 | **Agent 1 — Problem Generator** | Prompt engineering: sinh 5–10 bài toán theo chủ đề, đủ 3 cấp độ (Biết/Hiểu/Vận dụng) | 🔴 P0 |
| 5 | **Agent 2 — Solution Explainer** | Prompt engineering: nhận bài toán → giải + giải thích kiểu trẻ em hiểu được | 🔴 P0 |
| 6 | **Orchestrator / Pipeline** | Kết nối 2 agent: output của Agent 1 là input của Agent 2 | 🔴 P0 |
| 7 | **Hiển thị kết quả UI** | Render bài toán + lời giải đẹp, thân thiện với trẻ em (emoji, màu sắc) | 🟡 P1 |
| 8 | **Session state & UX** | Lưu kết quả trong session, nút "Tạo lại", loading spinner | 🟡 P1 |
| 9 | **Unit test agents** | Test prompt output hợp lệ, test pipeline, mock LLM calls | 🟡 P1 |
| 10 | **Deploy Streamlit Cloud** | Push lên GitHub, kết nối Streamlit Community Cloud, cấu hình secrets | 🟢 P2 |

### 7 Chủ đề toán lớp 4 trong hệ thống

| ID | Chủ đề | Kiến thức cốt lõi |
|----|--------|-------------------|
| T1 | Số tự nhiên | Đọc/viết/so sánh số đến 1 000 000, làm tròn |
| T2 | Bốn phép tính số tự nhiên | Cộng/Trừ/Nhân/Chia, thứ tự phép tính, biểu thức |
| T3 | Phân số — Khái niệm & tính chất | Rút gọn, quy đồng, so sánh phân số |
| T4 | Bốn phép tính phân số | Cộng/Trừ/Nhân/Chia phân số |
| T5 | Hình học | Góc, hình bình hành, hình thoi, hình thang — chu vi & diện tích |
| T6 | Đo lường | Quy đổi đơn vị độ dài, diện tích, khối lượng, thời gian |
| T7 | Toán có lời văn | Tổng–Hiệu, Tổng–Tỉ, trung bình cộng |

---

## 3. Thiết kế hệ thống

### Stack công nghệ

| Layer | Technology | Lý do chọn |
|---|---|---|
| **UI + App** | Python / Streamlit | All-in-one, deploy cloud miễn phí, phù hợp quy mô nhỏ |
| **LLM Provider** | Groq Cloud API | Miễn phí, cực nhanh (LPU), quota free đủ dùng cho 1–2 user |
| **LLM Model** | `llama-3.3-70b-versatile` (Groq) | Chất lượng cao, hỗ trợ tiếng Việt tốt, context 128k |
| **LLM SDK** | `groq` Python SDK (tương thích OpenAI SDK) | Dễ tích hợp, đổi model chỉ 1 dòng |
| **Prompt management** | Python strings / Jinja2 templates | Đơn giản, dễ chỉnh |
| **State** | `st.session_state` | Không cần DB, đủ cho 1–2 user |
| **Secrets** | `st.secrets` (production) / `.env` + `python-dotenv` (dev) | Bảo mật API key |
| **Deploy** | Streamlit Community Cloud | Free, gắn với GitHub repo |
| **Test** | pytest + `unittest.mock` | Mock LLM calls để test offline |

### Kiến trúc tổng thể

```
┌─────────────────────────────────────────────────────────┐
│                   STREAMLIT APP (app.py)                 │
│                                                         │
│  ┌──────────────┐    ┌─────────────────────────────┐   │
│  │  UI Layer    │    │     Orchestrator             │   │
│  │              │    │                             │   │
│  │ - Chọn chủ đề│───▶│  1. Gọi Agent 1             │   │
│  │ - Hiển thị   │    │     → nhận list bài toán    │   │
│  │   bài toán   │    │  2. Gọi Agent 2 (per bài)   │   │
│  │ - Hiển thị   │◀───│     → nhận lời giải         │   │
│  │   lời giải   │    │  3. Trả về cặp (bài, giải)  │   │
│  └──────────────┘    └──────────┬──────────────────┘   │
│                                 │                       │
└─────────────────────────────────│───────────────────────┘
                                  │ HTTP (Anthropic SDK)
                    ┌─────────────▼──────────────┐
                    │      Claude API             │
                    │  (claude-3-5-haiku/sonnet)  │
                    └────────────────────────────┘
```

### Luồng xử lý chi tiết

```
User chọn chủ đề (VD: "Phân số")
        │
        ▼
[Agent 1 — Problem Generator]
  Input : tên chủ đề + danh sách kiến thức cần bao phủ
  Output: JSON list gồm 5–8 bài toán
          {level: "biết|hiểu|vận_dụng", question: "...", hint: "..."}
        │
        ▼ (mỗi bài toán)
[Agent 2 — Solution Explainer]
  Input : 1 bài toán + level
  Output: {
    steps: ["Bước 1: ...", "Bước 2: ..."],
    answer: "...",
    explanation: "...",   ← giải thích kiểu trẻ em
    skill_note: "..."     ← ghi chú kỹ năng tư duy
  }
        │
        ▼
[UI Streamlit]
  Render từng cặp (bài toán + lời giải) theo dạng expander / card
```

---

## 4. Cấu trúc thư mục source code

```
source/backend/
├── app.py                     # Entry point Streamlit
├── agents/
│   ├── __init__.py
│   ├── problem_generator.py   # Agent 1: tạo bài toán
│   └── solution_explainer.py  # Agent 2: giải & giải thích
├── orchestrator.py            # Pipeline kết nối 2 agent
├── topics.py                  # Danh sách 7 chủ đề + kiến thức
├── prompts/
│   ├── problem_generator.j2   # Prompt template Agent 1
│   └── solution_explainer.j2  # Prompt template Agent 2
├── config.py                  # Cấu hình (model, max_tokens, v.v.)
├── utils.py                   # Helper: parse JSON output, retry logic
├── requirements.txt
├── .env.example               # Template biến môi trường
└── .streamlit/
    └── secrets.toml.example   # Template secrets cho Streamlit Cloud
```

---

## 5. Prompt Engineering — Chiến lược

### Agent 1 — Problem Generator

**Mục tiêu:** Sinh bài toán đa dạng, chuẩn chương trình lớp 4 Việt Nam, bao phủ đủ 3 cấp độ Bloom.

**Tiêu chí bài toán tốt:**
- **Biết**: Nhận biết, áp dụng công thức trực tiếp (tính toán đơn giản)
- **Hiểu**: Giải thích được tại sao, chuyển đổi giữa các dạng
- **Vận dụng**: Bài toán có lời văn, kết hợp nhiều bước, tình huống thực tế

**Output format:** JSON array để dễ parse và truyền sang Agent 2.

### Agent 2 — Solution Explainer

**Mục tiêu:** Giải thích như đang nói chuyện với em nhỏ — không dùng thuật ngữ khó, dùng hình ảnh quen thuộc (bánh pizza, kẹo, tiền xu...).

**Cấu trúc lời giải:**
1. **Đọc đề** — Tóm tắt bài toán bằng ngôn ngữ thật đơn giản
2. **Hướng tư duy** — "Chúng mình sẽ làm thế này nhé..."
3. **Từng bước** — Mỗi bước ngắn gọn, có ví dụ hình ảnh
4. **Kết quả** — Trả lời câu hỏi đề bài
5. **Kỹ năng học được** — 1 câu tóm tắt kỹ năng tư duy

---

## 6. Testing

- **Unit test**: pytest + mock — đặt tại `unittest/backend/`
- **Test Agent 1**: Verify output là valid JSON, đủ 3 level, đúng chủ đề
- **Test Agent 2**: Verify output có đủ fields, không rỗng
- **Test Orchestrator**: End-to-end với mock LLM responses
- **Output**: báo cáo tại `unittest/output/`

```bash
# Chạy test (mock LLM, không tốn API credit)
cd unittest
pytest backend/ -v --html=output/report.html --self-contained-html
```

---

## 7. Deploy lên Streamlit Community Cloud

### Bước deploy

```bash
# 1. Push code lên GitHub (repo public hoặc private)
git push origin main

# 2. Vào https://share.streamlit.io
# 3. New app → chọn repo → branch: main → file: source/backend/app.py
# 4. Advanced settings → Secrets → dán nội dung .streamlit/secrets.toml
```

### Checklist deploy
- [ ] `GROQ_API_KEY` đã set trong Streamlit Secrets (không commit key thật)
- [ ] `requirements.txt` đầy đủ và pin version
- [ ] Test chạy offline pass hết
- [ ] Không có `print()` debug còn sót
- [ ] Spinner / loading state hoạt động đúng
- [ ] Lỗi LLM được bắt và hiển thị thông báo thân thiện

---

## 8. Quy tắc làm việc với Claude

1. **Luôn đọc** `PROJECT_REQUIREMENTS.md` trước khi implement
2. **Prompt là tài sản quan trọng nhất** — chỉnh sửa prompt phải test kỹ
3. **Không hard-code API key** — luôn đọc `GROQ_API_KEY` từ `st.secrets` hoặc `os.environ`
4. **Parse JSON output của LLM cẩn thận** — dùng `try/except`, có fallback
5. **Mock LLM khi test** — không gọi API thật trong unit test
6. **Cập nhật** `docs/overview.html` khi hoàn thành từng module
