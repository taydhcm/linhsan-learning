# CLAUDE.md — Tổng quan dự án linhsan-learning

> File này là nguồn thông tin chính cho Claude AI khi làm việc với dự án này.  
> Đọc kỹ toàn bộ trước khi thực hiện bất kỳ thay đổi nào.

---

## 1. Dự án là gì?

**linhsan-learning** là một ứng dụng web học tập thông minh dành cho học sinh lớp 4 Việt Nam (9–10 tuổi), được triển khai trên **Streamlit Community Cloud**. Hệ thống hỗ trợ **2 môn học**: **Toán** và **Tiếng Việt**, mỗi môn đều dùng **2 AI Agent** phối hợp:

1. **Agent tạo câu hỏi / bài toán** — Sinh nội dung ôn tập phù hợp với chủ đề người dùng chọn, đảm bảo bao phủ 3 cấp độ tư duy: Nhận biết → Thông hiểu → Vận dụng.
2. **Agent giải & giải thích** — Giải từng câu hỏi/bài toán theo phong cách cực kỳ đơn giản, dễ hiểu như đang nói chuyện với một bạn nhỏ 5–6 tuổi; đồng thời định hình tư duy và kỹ năng môn học cho trẻ.

**Giao diện:** Tab chọn môn (🧮 Toán | 📖 Tiếng Việt) → chọn chủ đề → nhận bộ câu hỏi + lời giải.

Quy mô: **nhỏ gọn, 1–2 người dùng**, không cần database, không cần auth phức tạp.

---

## 2. Chúng ta cần làm gì?

### Danh sách TODO — v2.0 (Toán, đã DONE) + v3.0 (Tiếng Việt, cần implement)

#### ✅ v2.0 — Module Toán (đã hoàn thành)

| # | Hạng mục | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| 1 | **Setup project Streamlit** | Tạo `app.py`, cấu trúc thư mục, `requirements.txt` | 🔴 P0 | ✅ DONE |
| 2 | **Cấu hình LLM API** | Tích hợp Groq SDK, đọc key từ `st.secrets` / `.env` | 🔴 P0 | ✅ DONE |
| 3 | **UI chọn chủ đề Toán** | Dropdown chọn 1 trong 7 chủ đề toán lớp 4 | 🔴 P0 | ✅ DONE |
| 4 | **Agent 1 — Problem Generator (Toán)** | Sinh 6 bài toán, đủ 3 cấp độ (Biết/Hiểu/Vận dụng), output JSON | 🔴 P0 | ✅ DONE |
| 5 | **Agent 2 — Solution Explainer (Toán)** | Nhận bài toán → giải + giải thích kiểu trẻ em, output JSON | 🔴 P0 | ✅ DONE |
| 6 | **Orchestrator / Pipeline (Toán)** | Kết nối 2 agent: output Agent 1 → input Agent 2 | 🔴 P0 | ✅ DONE |
| 7 | **Hiển thị kết quả UI** | Expander/card, thân thiện trẻ em, ẩn/hiện lời giải | 🟡 P1 | ✅ DONE |
| 8 | **Session state & UX** | Lưu session, nút "Tạo lại", spinner | 🟡 P1 | ✅ DONE |
| 9 | **Unit test agents (Toán)** | Test prompt output, pipeline, mock LLM | 🟡 P1 | ✅ DONE |
| 10 | **Deploy Streamlit Cloud** | Push GitHub, kết nối Streamlit Cloud, cấu hình secrets | 🟢 P2 | ✅ DONE |
| 11 | **iOS compatibility fix** | `enableWebsocketCompression = false` trong `.streamlit/config.toml` | 🟢 P2 | ✅ DONE |

#### 🔲 v3.0 — Module Tiếng Việt (cần implement)

| # | Hạng mục | Mô tả | Ưu tiên | Trạng thái |
|---|---|---|---|---|
| 12 | **UI tab Toán / Tiếng Việt** | Thêm `st.tabs(["🧮 Toán", "📖 Tiếng Việt"])` vào `app.py`; tái cấu trúc layout | 🔴 P0 | ⬜ TODO |
| 13 | **vietnamese_topics.py** | Định nghĩa 7 chủ đề Tiếng Việt lớp 4 + danh sách kỹ năng từng chủ đề | 🔴 P0 | ⬜ TODO |
| 14 | **Agent 1 — Question Generator (Tiếng Việt)** | Sinh 6 câu hỏi ôn tập theo chủ đề TV, 3 cấp độ, output JSON | 🔴 P0 | ⬜ TODO |
| 15 | **Agent 2 — Answer Explainer (Tiếng Việt)** | Nhận câu hỏi → giải thích đáp án kiểu trẻ em + định hình kỹ năng TV | 🔴 P0 | ⬜ TODO |
| 16 | **Orchestrator Tiếng Việt** | Pipeline riêng hoặc mở rộng orchestrator hiện có cho module TV | 🔴 P0 | ⬜ TODO |
| 17 | **Unit test agents Tiếng Việt** | Mock LLM, test JSON schema, test pipeline TV | 🟡 P1 | ⬜ TODO |

### 7 Chủ đề Toán lớp 4

| ID | Chủ đề | Kiến thức cốt lõi |
|----|--------|-------------------|
| T1 | Số tự nhiên | Đọc/viết/so sánh số đến 1 000 000, làm tròn |
| T2 | Bốn phép tính số tự nhiên | Cộng/Trừ/Nhân/Chia, thứ tự phép tính, biểu thức |
| T3 | Phân số — Khái niệm & tính chất | Rút gọn, quy đồng, so sánh phân số |
| T4 | Bốn phép tính phân số | Cộng/Trừ/Nhân/Chia phân số |
| T5 | Hình học | Góc, hình bình hành, hình thoi, hình thang — chu vi & diện tích |
| T6 | Đo lường | Quy đổi đơn vị độ dài, diện tích, khối lượng, thời gian |
| T7 | Toán có lời văn | Tổng–Hiệu, Tổng–Tỉ, trung bình cộng |

### 7 Chủ đề Tiếng Việt lớp 4 (module mới)

| ID | Chủ đề | Kỹ năng cần bao phủ |
|----|--------|---------------------|
| V1 | Tập đọc — Đọc hiểu | Tìm ý chính, nhân vật, thái độ tác giả, chi tiết quan trọng |
| V2 | Từ loại | Danh từ/Động từ/Tính từ/Đại từ — nhận biết, phân loại, đặt câu |
| V3 | Cấu tạo từ | Từ đơn, từ ghép (tổng hợp/phân loại), từ láy (âm/vần/tiếng) |
| V4 | Cấu tạo câu | Chủ ngữ–Vị ngữ–Trạng ngữ; câu kể/hỏi/cảm/khiến; dấu câu |
| V5 | Chính tả | Phân biệt l/n, r/d/gi, s/x, ch/tr; viết hoa danh từ riêng |
| V6 | Văn kể chuyện | Cấu trúc 3 phần, xây dựng nhân vật, diễn biến, kết thúc |
| V7 | Văn miêu tả | Tả đồ vật/cây cối/con vật; trình tự quan sát; dùng so sánh, nhân hóa |

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

### Kiến trúc tổng thể (v3.0)

```
┌──────────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP (app.py)                         │
│                                                                  │
│  st.tabs(["🧮 Toán", "📖 Tiếng Việt"])                            │
│       │                          │                               │
│  ┌────▼──────┐             ┌─────▼──────┐                        │
│  │ Tab Toán  │             │ Tab TV     │                        │
│  │           │             │            │                        │
│  │ Chọn T1–T7│             │ Chọn V1–V7 │                        │
│  └────┬──────┘             └─────┬──────┘                        │
│       │                          │                               │
│  ┌────▼──────────┐        ┌──────▼──────────┐                   │
│  │ Orchestrator  │        │ OrchestratorViet│                   │
│  │  (Toán)       │        │  (Tiếng Việt)   │                   │
│  │ Agent1→Agent2 │        │ AgentV1→AgentV2 │                   │
│  └────┬──────────┘        └──────┬──────────┘                   │
└───────│───────────────────────────│──────────────────────────────┘
        │                           │  Groq SDK (HTTP)
        └──────────────┬────────────┘
                ┌──────▼───────────────────┐
                │  Groq Cloud API           │
                │  llama-3.3-70b-versatile  │
                └──────────────────────────┘
```

### Luồng xử lý — Module Toán

```
User chọn chủ đề Toán (VD: "Phân số")
        │
        ▼
[Agent 1 — Problem Generator]
  Input : tên chủ đề + danh sách kiến thức
  Output: JSON list [{id, level, question, hint}]
        │
        ▼ (mỗi bài)
[Agent 2 — Solution Explainer]
  Output: {steps[], answer, explanation, skill_note}
        │
        ▼
[UI] Render expander — tiêu đề = đề bài đầy đủ, mặc định thu gọn
```

### Luồng xử lý — Module Tiếng Việt

```
User chọn chủ đề Tiếng Việt (VD: "Từ loại")
        │
        ▼
[Agent 1 — Question Generator (TV)]
  Input : tên chủ đề + danh sách kỹ năng cần bao phủ
  Output: JSON list [{id, level, type, question, hint}]
          level: "nhận_biết | thông_hiểu | vận_dụng"
          type : "trắc_nghiệm | tự_luận | điền_chỗ_trống"
        │
        ▼ (mỗi câu hỏi)
[Agent 2 — Answer Explainer (TV)]
  Output: {
    read_question: "Bài này hỏi gì...",
    thinking_direction: "Chúng mình sẽ...",
    steps: ["Bước 1..."],
    answer: "Đáp án...",
    explanation: "Giải thích hình ảnh dễ hiểu...",
    skill_note: "Kỹ năng Tiếng Việt học được..."
  }
        │
        ▼
[UI] Render giống Tab Toán — expander, thu gọn mặc định
```

---

## 4. Cấu trúc thư mục source code

```
source/backend/
├── app.py                          # Entry point Streamlit — st.tabs([Toán, TV])
├── agents/
│   ├── __init__.py
│   ├── problem_generator.py        # Agent 1 Toán: tạo bài toán
│   ├── solution_explainer.py       # Agent 2 Toán: giải & giải thích
│   ├── viet_question_generator.py  # Agent 1 TV: tạo câu hỏi Tiếng Việt  ← MỚI
│   └── viet_answer_explainer.py    # Agent 2 TV: giải thích đáp án TV     ← MỚI
├── orchestrator.py                 # Pipeline Toán (Agent1 → Agent2)
├── orchestrator_viet.py            # Pipeline Tiếng Việt (AgentV1 → AgentV2) ← MỚI
├── topics.py                       # 7 chủ đề Toán + kiến thức
├── vietnamese_topics.py            # 7 chủ đề Tiếng Việt + kỹ năng          ← MỚI
├── prompts/
│   ├── problem_generator.j2        # Prompt Agent 1 Toán
│   ├── solution_explainer.j2       # Prompt Agent 2 Toán
│   ├── viet_question_generator.j2  # Prompt Agent 1 TV                     ← MỚI
│   └── viet_answer_explainer.j2    # Prompt Agent 2 TV                     ← MỚI
├── config.py                       # Cấu hình (model, max_tokens, v.v.)
├── utils.py                        # Helper: parse JSON output, retry logic
├── requirements.txt
├── .env.example                    # Template biến môi trường
└── .streamlit/
    ├── config.toml                 # enableWebsocketCompression = false (iOS fix)
    └── secrets.toml.example        # Template secrets cho Streamlit Cloud
```

---

## 5. Prompt Engineering — Chiến lược

### Agent 1 Toán — Problem Generator

**Mục tiêu:** Sinh bài toán đa dạng, chuẩn chương trình lớp 4 Việt Nam, bao phủ đủ 3 cấp độ Bloom.

**Tiêu chí bài toán tốt:**
- **Biết**: Nhận biết, áp dụng công thức trực tiếp (tính toán đơn giản)
- **Hiểu**: Giải thích được tại sao, chuyển đổi giữa các dạng
- **Vận dụng**: Bài toán có lời văn, kết hợp nhiều bước, tình huống thực tế

**Output format:** JSON array `[{id, level, question, hint}]`

### Agent 2 Toán — Solution Explainer

**Mục tiêu:** Giải thích như đang nói chuyện với em nhỏ — không dùng thuật ngữ khó, dùng hình ảnh quen thuộc (bánh pizza, kẹo, tiền xu...).

**Output format:** JSON `{problem_id, read_problem, thinking_direction, steps[], answer, explanation, skill_note}`

---

### Agent 1 TV — Question Generator (Tiếng Việt)

**Mục tiêu:** Sinh câu hỏi ôn tập Tiếng Việt đa dạng, chuẩn SGK lớp 4, bao phủ 3 cấp độ Bloom theo từng chủ đề.

**Tiêu chí câu hỏi tốt:**
- **Nhận biết**: Nhận ra từ loại, xác định thành phần câu, chọn đáp án đúng/sai
- **Thông hiểu**: Giải thích nghĩa, phân tích cấu tạo, so sánh hai trường hợp
- **Vận dụng**: Đặt câu, viết đoạn văn ngắn, sửa lỗi sai trong câu cho sẵn

**Dạng câu hỏi (type):**
- `trắc_nghiệm` — 4 lựa chọn A/B/C/D
- `tự_luận` — viết câu / đoạn văn ngắn
- `điền_chỗ_trống` — điền từ thích hợp vào chỗ trống

**Output format:** JSON array `[{id, level, type, question, hint}]`

### Agent 2 TV — Answer Explainer (Tiếng Việt)

**Mục tiêu:** Giải thích đáp án bằng ngôn ngữ thật đơn giản — như nói chuyện với bé 5 tuổi. Định hình tư duy ngôn ngữ và kỹ năng Tiếng Việt lâu dài.

**Nguyên tắc giải thích TV:**
- Dùng ví dụ từ cuộc sống hàng ngày của trẻ (trường học, gia đình, đồ chơi)
- Giải thích "tại sao" chứ không chỉ "là gì"
- So sánh trường hợp đúng / sai để bé dễ phân biệt
- Kết thúc bằng kỹ năng Tiếng Việt mà bé học được

**Output format:** JSON `{question_id, read_question, thinking_direction, steps[], answer, explanation, skill_note}`

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
