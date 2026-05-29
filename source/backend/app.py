"""
app.py — Entry point Streamlit cho linhsan-learning v3.0.
         Hỗ trợ 2 môn: 🧮 Toán và 📖 Tiếng Việt

Chạy: streamlit run app.py  (từ thư mục source/backend/)
"""

import streamlit as st
from config import get_groq_api_key
from topics import TOPICS
from vietnamese_topics import VIET_TOPICS
from orchestrator import Orchestrator
from orchestrator_viet import OrchestratorViet

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📚 Linhsan Learning — AI Tutor lớp 4",
    page_icon="📚",
    layout="centered",
)

# ── CSS thân thiện trẻ em ──────────────────────────────────────────────────────
st.markdown("""
<style>
  .problem-card {
    background: #fff9f0;
    border-left: 5px solid #ff9800;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 1.05em;
  }
  .viet-card {
    background: #f0fff4;
    border-left: 5px solid #43a047;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 1.05em;
  }
  .step-item {
    background: #f0f4ff;
    border-radius: 6px;
    padding: 8px 14px;
    margin: 4px 0;
  }
  .type-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.78em;
    font-weight: 600;
    background: #e8f5e9;
    color: #2e7d32;
    margin-left: 6px;
  }
  .level-badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 0.82em;
    font-weight: 700;
  }
</style>
""", unsafe_allow_html=True)

# ── Validate API key khi khởi động ────────────────────────────────────────────
try:
    get_groq_api_key()
except EnvironmentError as exc:
    st.error(
        f"⚠️ **Thiếu GROQ_API_KEY!**\n\n{exc}\n\n"
        "Lấy key miễn phí tại [console.groq.com](https://console.groq.com)"
    )
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("📚 Linhsan Learning — AI Tutor lớp 4")
st.caption("Chọn môn học → chọn chủ đề → AI tạo bài và giải thích thật dễ hiểu cho bé! 🌟")
st.divider()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_toan, tab_viet = st.tabs(["🧮 Toán", "📖 Tiếng Việt"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB TOÁN
# ══════════════════════════════════════════════════════════════════════════════
def render_toan_result(solution: dict):
    if not solution:
        st.warning("⚠️ Không thể tạo lời giải cho bài này. Bạn thử lại nhé!")
        return
    if solution.get("read_problem"):
        st.markdown("**🔍 Bài này hỏi gì?**")
        st.markdown(f"> {solution['read_problem']}")
    if solution.get("thinking_direction"):
        st.markdown("**🧭 Hướng giải:**")
        st.markdown(f"*{solution['thinking_direction']}*")
    steps: list = solution.get("steps", [])
    if steps:
        st.markdown("**📌 Các bước giải:**")
        for step in steps:
            st.markdown(f'<div class="step-item">▶ {step}</div>', unsafe_allow_html=True)
    if solution.get("answer"):
        st.success(f"🎉 **Đáp án:** {solution['answer']}")
    if solution.get("explanation"):
        st.markdown(f"**🍭 Giải thích dễ hiểu hơn:**\n\n{solution['explanation']}")
    if solution.get("skill_note"):
        st.info(f"🧠 **Kỹ năng tư duy học được:** {solution['skill_note']}")


with tab_toan:
    LEVEL_CONFIG_TOAN = {
        "biết":     "🟦 Biết",
        "hiểu":     "🟧 Hiểu",
        "vận_dụng": "🟥 Vận dụng",
    }
    topic_map: dict[str, dict] = {t["name"]: t for t in TOPICS}
    selected_name: str = st.selectbox(
        "📚 Chọn chủ đề Toán:",
        options=list(topic_map.keys()),
        index=0,
        key="toan_topic",
    )
    selected_topic = topic_map[selected_name]
    with st.expander("📖 Kiến thức bao phủ trong chủ đề này", expanded=False):
        for k in selected_topic["knowledge"]:
            st.markdown(f"- {k}")
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        start_toan = st.button("🚀 Bắt đầu học!", use_container_width=True, type="primary", key="btn_toan_start")
    with col2:
        has_toan = bool(st.session_state.get("toan_results"))
        retry_toan = st.button("🔄 Tạo lại", use_container_width=True, disabled=not has_toan, key="btn_toan_retry")

    if start_toan or retry_toan:
        st.session_state["toan_results"] = None
        st.session_state["toan_topic_current"] = selected_topic
        with st.spinner("🤖 AI đang tạo bài toán và lời giải... (khoảng 20–40 giây)"):
            try:
                st.session_state["toan_results"] = Orchestrator().run(selected_topic)
            except Exception as exc:
                st.error(f"😅 Ối, gặp sự cố rồi! Bạn thử lại nhé 🙂\n\nChi tiết lỗi: `{exc}`")
                st.stop()

    toan_results: list[dict] | None = st.session_state.get("toan_results")
    if toan_results:
        current = st.session_state.get("toan_topic_current", {})
        st.success(f"✅ Đã tạo **{len(toan_results)} bài toán** về chủ đề **{current.get('name', '')}**!")
        st.divider()
        for i, item in enumerate(toan_results, start=1):
            problem = item.get("problem", {})
            solution = item.get("solution", {})
            level = problem.get("level", "biết")
            label = LEVEL_CONFIG_TOAN.get(level, "🟦 Biết")
            full_question = problem.get("question", "")
            with st.expander(f"Bài {i} | {label} — {full_question}", expanded=False):
                st.markdown(
                    f'<div class="problem-card"><strong>📝 Đề bài:</strong><br><br>{full_question}</div>',
                    unsafe_allow_html=True,
                )
                if problem.get("hint"):
                    st.caption(f"💡 **Gợi ý:** {problem['hint']}")
                st.markdown("---")
                render_toan_result(solution)
        st.divider()
        st.markdown("💪 **Cố lên!** Làm nhiều bài toán mỗi ngày, bé sẽ ngày càng giỏi hơn! ⭐")
    else:
        st.markdown("""
### Hướng dẫn sử dụng
1. 📚 **Chọn chủ đề** Toán bạn muốn ôn tập
2. 🚀 Nhấn **"Bắt đầu học!"** và chờ AI tạo bài
3. 📝 Đọc từng **đề bài**, thử tự giải trước
4. 👁️ Mở xem **lời giải** để kiểm tra và học cách giải
> 🌟 Mỗi lần tạo sẽ có bộ bài toán MỚI — bấm "Tạo lại" để luyện thêm!
        """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB TIẾNG VIỆT
# ══════════════════════════════════════════════════════════════════════════════
def render_viet_result(explanation: dict):
    if not explanation:
        st.warning("⚠️ Không thể tạo lời giải thích cho câu này. Bạn thử lại nhé!")
        return
    if explanation.get("read_question"):
        st.markdown("**🔍 Câu hỏi này hỏi gì?**")
        st.markdown(f"> {explanation['read_question']}")
    if explanation.get("thinking_direction"):
        st.markdown("**🧭 Hướng tìm đáp án:**")
        st.markdown(f"*{explanation['thinking_direction']}*")
    steps: list = explanation.get("steps", [])
    if steps:
        st.markdown("**📌 Các bước phân tích:**")
        for step in steps:
            st.markdown(f'<div class="step-item">▶ {step}</div>', unsafe_allow_html=True)
    if explanation.get("answer"):
        st.success(f"🎉 **Đáp án:** {explanation['answer']}")
    if explanation.get("explanation"):
        st.markdown(f"**🍭 Giải thích dễ hiểu hơn:**\n\n{explanation['explanation']}")
    if explanation.get("skill_note"):
        st.info(f"📝 **Kỹ năng Tiếng Việt học được:** {explanation['skill_note']}")


with tab_viet:
    LEVEL_CONFIG_VIET = {
        "nhận_biết":  "🟦 Nhận biết",
        "thông_hiểu": "🟧 Thông hiểu",
        "vận_dụng":   "🟥 Vận dụng",
    }
    TYPE_LABELS = {
        "trắc_nghiệm":    "Trắc nghiệm",
        "tự_luận":        "Tự luận",
        "điền_chỗ_trống": "Điền chỗ trống",
    }
    viet_topic_map: dict[str, dict] = {t["name"]: t for t in VIET_TOPICS}
    selected_viet_name: str = st.selectbox(
        "📚 Chọn chủ đề Tiếng Việt:",
        options=list(viet_topic_map.keys()),
        index=0,
        key="viet_topic",
    )
    selected_viet_topic = viet_topic_map[selected_viet_name]
    with st.expander("📖 Kỹ năng bao phủ trong chủ đề này", expanded=False):
        for s in selected_viet_topic["skills"]:
            st.markdown(f"- {s}")
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        start_viet = st.button("🚀 Bắt đầu học!", use_container_width=True, type="primary", key="btn_viet_start")
    with col2:
        has_viet = bool(st.session_state.get("viet_results"))
        retry_viet = st.button("🔄 Tạo lại", use_container_width=True, disabled=not has_viet, key="btn_viet_retry")

    if start_viet or retry_viet:
        st.session_state["viet_results"] = None
        st.session_state["viet_topic_current"] = selected_viet_topic
        with st.spinner("🤖 AI đang tạo câu hỏi và lời giải thích... (khoảng 20–40 giây)"):
            try:
                st.session_state["viet_results"] = OrchestratorViet().run(selected_viet_topic)
            except Exception as exc:
                st.error(f"😅 Ối, gặp sự cố rồi! Bạn thử lại nhé 🙂\n\nChi tiết lỗi: `{exc}`")
                st.stop()

    viet_results: list[dict] | None = st.session_state.get("viet_results")
    if viet_results:
        current_viet = st.session_state.get("viet_topic_current", {})
        st.success(f"✅ Đã tạo **{len(viet_results)} câu hỏi** về chủ đề **{current_viet.get('name', '')}**!")
        st.divider()
        for i, item in enumerate(viet_results, start=1):
            question = item.get("question", {})
            explanation = item.get("explanation", {})
            level = question.get("level", "nhận_biết")
            qtype = question.get("type", "tự_luận")
            label = LEVEL_CONFIG_VIET.get(level, "🟦 Nhận biết")
            type_label = TYPE_LABELS.get(qtype, qtype)
            full_question = question.get("question", "")
            with st.expander(f"Câu {i} | {label} — {full_question}", expanded=False):
                st.markdown(
                    f'<div class="viet-card"><strong>📝 Câu hỏi:</strong>'
                    f'<span class="type-badge">{type_label}</span>'
                    f'<br><br>{full_question}</div>',
                    unsafe_allow_html=True,
                )
                if question.get("hint"):
                    st.caption(f"💡 **Gợi ý:** {question['hint']}")
                st.markdown("---")
                render_viet_result(explanation)
        st.divider()
        st.markdown("💪 **Cố lên!** Luyện Tiếng Việt mỗi ngày, bé sẽ viết văn hay hơn! ⭐")
    else:
        st.markdown("""
### Hướng dẫn sử dụng
1. 📚 **Chọn chủ đề** Tiếng Việt bạn muốn ôn tập
2. 🚀 Nhấn **"Bắt đầu học!"** và chờ AI tạo câu hỏi
3. 📝 Đọc từng **câu hỏi**, thử trả lời trước
4. 👁️ Mở xem **lời giải thích** để kiểm tra và học kỹ năng TV
> 🌟 Mỗi lần tạo sẽ có bộ câu hỏi MỚI — bấm "Tạo lại" để luyện thêm!
        """)
