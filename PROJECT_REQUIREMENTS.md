# PROJECT_REQUIREMENTS.md — Yêu cầu dự án linhsan-learning

> File này mô tả toàn bộ yêu cầu nghiệp vụ và kỹ thuật của dự án.  
> Claude phải đọc file này trước khi implement bất kỳ chức năng nào.  
> Cập nhật lần cuối: 2026-05-29

---

## 1. Thông tin dự án

| Thuộc tính        | Giá trị                                                            |
|-------------------|--------------------------------------------------------------------|
| Tên dự án         | linhsan-learning                                                   |
| Loại              | AI-powered Math Learning App (2 Agents)                            |
| Phiên bản         | 1.0.0                                                              |
| Đối tượng sử dụng | Học sinh lớp 4 Việt Nam (9–10 tuổi), phụ huynh hỗ trợ             |
| Quy mô            | Nhỏ, 1–2 người dùng đồng thời                                      |
| Phạm vi           | Web app đơn trang, deploy trên Streamlit Community Cloud           |
| Không bao gồm     | Auth, database, thanh toán, multi-user, mobile native app          |

---

## 2. Yêu cầu chức năng

### 2.1 UI — Chọn chủ đề học

| ID | User Story | Tiêu chí nghiệm thu |
|----|------------|---------------------|
| UI-01 | Người dùng muốn xem danh sách 7 chủ đề toán lớp 4 để chọn | Hiển thị đủ 7 chủ đề với mô tả ngắn, giao diện thân thiện |
| UI-02 | Người dùng muốn chọn 1 chủ đề và nhấn "Bắt đầu học" | Nút rõ ràng, disable khi đang xử lý, có loading indicator |
| UI-03 | Người dùng muốn tạo lại bộ bài toán mới cho cùng chủ đề | Nút "Tạo lại" xuất hiện sau khi có kết quả đầu tiên |
| UI-04 | Người dùng muốn xem lời giải của từng bài (có thể ẩn/hiện) | Accordion/expander cho từng bài, mặc định ẩn lời giải |

### 2.2 Agent 1 — Problem Generator (Tạo bài toán)

| ID | User Story | Tiêu chí nghiệm thu |
|----|------------|---------------------|
| AG1-01 | Hệ thống sinh ra 5–8 bài toán khi người dùng chọn chủ đề | Đúng số lượng, đúng chủ đề, không lặp lại |
| AG1-02 | Bài toán phải bao phủ đủ 3 cấp độ: Biết / Hiểu / Vận dụng | Mỗi cấp độ ít nhất 1 bài, có nhãn level rõ ràng |
| AG1-03 | Bài toán phù hợp lứa tuổi: ngôn ngữ đơn giản, số không quá lớn | Reviewer (người lớn) xác nhận phù hợp chương trình lớp 4 |
| AG1-04 | Output là JSON hợp lệ, có thể parse tự động | `json.loads()` không throw exception; có fallback khi LLM trả lỗi |
| AG1-05 | Mỗi bài toán có thêm gợi ý (hint) ngắn | Gợi ý không tiết lộ đáp án, giúp bé tự suy nghĩ |

**Output schema của Agent 1:**
```json
[
  {
    "id": 1,
    "level": "biết | hiểu | vận_dụng",
    "question": "Nội dung bài toán...",
    "hint": "Gợi ý ngắn..."
  }
]
```

### 2.3 Agent 2 — Solution Explainer (Giải & giải thích)

| ID | User Story | Tiêu chí nghiệm thu |
|----|------------|---------------------|
| AG2-01 | Với mỗi bài toán, hệ thống sinh lời giải chi tiết từng bước | Đủ số bước, không bỏ qua bước nào |
| AG2-02 | Giải thích dùng ngôn ngữ trẻ em hiểu được (như nói chuyện với bé 5 tuổi) | Không có thuật ngữ hàn lâm; dùng hình ảnh thực tế (kẹo, pizza, tiền…) |
| AG2-03 | Mỗi lời giải có phần "kỹ năng tư duy" để định hình tư duy cho bé | Field `skill_note` không rỗng, có giá trị giáo dục |
| AG2-04 | Đáp án cuối phải đúng về mặt toán học | Kết quả số học chính xác 100% |
| AG2-05 | Output là JSON hợp lệ | `json.loads()` không throw exception; có fallback khi parse lỗi |

**Output schema của Agent 2:**
```json
{
  "problem_id": 1,
  "read_problem": "Tóm tắt bài toán bằng ngôn ngữ thật đơn giản...",
  "thinking_direction": "Chúng mình sẽ làm thế này nhé...",
  "steps": [
    "Bước 1: ...",
    "Bước 2: ..."
  ],
  "answer": "Kết quả cuối cùng là...",
  "explanation": "Giải thích bằng hình ảnh quen thuộc...",
  "skill_note": "Kỹ năng tư duy học được từ bài này..."
}
```

### 2.4 Orchestrator — Pipeline kết nối 2 Agent

| ID | User Story | Tiêu chí nghiệm thu |
|----|------------|---------------------|
| ORC-01 | Khi người dùng chọn chủ đề, hệ thống tự động chạy Agent 1 rồi Agent 2 | Không cần thao tác thêm từ người dùng |
| ORC-02 | Kết quả hiển thị từng bài ngay khi có (streaming hoặc batch) | Người dùng thấy phản hồi trong ≤ 30 giây |
| ORC-03 | Lỗi LLM (timeout, rate limit) được xử lý gracefully | Hiển thị thông báo thân thiện, có nút thử lại |
| ORC-04 | Retry tối đa 3 lần khi LLM trả về output không hợp lệ | Sau 3 lần thất bại mới báo lỗi cho user |

### 2.5 Session State & UX

| ID | User Story | Tiêu chí nghiệm thu |
|----|------------|---------------------|
| UX-01 | Kết quả (bài toán + lời giải) được lưu trong session — không mất khi scroll | `st.session_state` lưu đúng, reload không mất dữ liệu trong session |
| UX-02 | Spinner / progress hiển thị trong khi chờ LLM trả về | Người dùng biết hệ thống đang xử lý |
| UX-03 | Giao diện thân thiện với trẻ em: màu sắc tươi, emoji, font dễ đọc | Không có text nhỏ hơn 14px, contrast đủ chuẩn |

---

## 3. Yêu cầu phi chức năng

### 3.1 Hiệu năng
- Tổng thời gian sinh bài toán + lời giải: ≤ 60 giây (chấp nhận được vì LLM call)
- Streamlit app load ban đầu: ≤ 5 giây
- Không block UI trong khi chờ LLM (dùng `st.spinner`)

### 3.2 Bảo mật
- **API key tuyệt đối không commit lên Git** — đọc từ `st.secrets` (prod) hoặc `.env` (dev)
- Không log nội dung người dùng hoặc API key ra console / file
- Không có thông tin nhạy cảm trong URL params
- Sử dụng HTTPS (do Streamlit Cloud cung cấp tự động)

### 3.3 Độ tin cậy
- Xử lý `json.JSONDecodeError` khi LLM trả về text không phải JSON hợp lệ
- Timeout cho mỗi LLM call: 60 giây
- Fallback message thân thiện khi có lỗi: *"Ối, mình gặp sự cố rồi! Bạn thử lại nhé 🙂"*

### 3.4 Khả năng bảo trì
- Code coverage ≥ 70% (unit test với mock LLM)
- Mỗi agent là 1 class/module riêng biệt, dễ thay đổi prompt độc lập
- Prompt template tách ra file `.j2` riêng — không embed trong code

---

## 4. Ràng buộc kỹ thuật

| Thành phần | Yêu cầu bắt buộc |
|------------|------------------|
| Python | ≥ 3.11 |
| Streamlit | ≥ 1.35 |
| groq SDK | ≥ 0.9 (`pip install groq`) |
| python-dotenv | ≥ 1.0 (đọc `.env` ở local dev) |
| Jinja2 | ≥ 3.1 (render prompt template) |
| pytest | ≥ 8.0 (unit test) |
| Deploy target | Streamlit Community Cloud (streamlit.app) |
| LLM Provider | Groq Cloud (console.groq.com) — free tier |
| LLM Model chính | `llama-3.3-70b-versatile` (nhanh, chất lượng cao) |
| LLM Model fallback | `llama-3.1-8b-instant` (nhẹ hơn, nếu cần tiết kiệm quota) |

---

## 5. Danh sách 7 chủ đề toán lớp 4

| ID | Tên chủ đề | Kiến thức cần bao phủ |
|----|------------|----------------------|
| T1 | Số tự nhiên | Đọc/viết số đến 1 000 000; so sánh; làm tròn số |
| T2 | Bốn phép tính số tự nhiên | Cộng/Trừ/Nhân/Chia; thứ tự thực hiện phép tính; biểu thức có ngoặc |
| T3 | Phân số — Khái niệm & tính chất | Khái niệm phân số; rút gọn; quy đồng mẫu số; so sánh phân số |
| T4 | Bốn phép tính phân số | Cộng/Trừ/Nhân/Chia phân số; hỗn số |
| T5 | Hình học | Góc nhọn/tù/vuông/bẹt; hình bình hành, hình thoi, hình thang — chu vi & diện tích |
| T6 | Đo lường | Quy đổi đơn vị độ dài, diện tích (ha, km²), khối lượng, thời gian |
| T7 | Toán có lời văn | Bài toán Tổng–Hiệu; Tổng–Tỉ; trung bình cộng; bài toán thực tế |

---

## 6. Tiêu chí nghiệm thu (Definition of Done)

Một module/chức năng được coi là **DONE** khi:

- [ ] Chức năng hoạt động đúng theo user story
- [ ] Unit test đã viết và pass (với mock LLM)
- [ ] Không có lỗi lint (`flake8` hoặc `ruff`)
- [ ] Không có API key / secret hard-coded
- [ ] Lỗi LLM được bắt và hiển thị thông báo thân thiện
- [ ] Trạng thái trong `docs/overview.html` cập nhật thành "Done"

---

## 7. Lịch sử thay đổi

| Phiên bản | Ngày       | Nội dung                                              |
|-----------|------------|-------------------------------------------------------|
| 1.0.0     | 2026-05-29 | Khởi tạo tài liệu — E-learning platform chung         |
| 2.0.0     | 2026-05-29 | Rewrite toàn bộ — AI 2-agent Math learning cho lớp 4  |
