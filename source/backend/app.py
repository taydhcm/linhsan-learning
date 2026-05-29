"""
app.py — Entry point Streamlit cho linhsan-learning.

Chạy: streamlit run app.py  (từ thư mục source/backend/)
"""

import streamlit as st
from config import get_groq_api_key
from topics import TOPICS
from orchestrator import Orchestrator

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🧮 Toán lớp 4 — AI Tutor",
    page_icon="🧮",
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
  .step-item {
    background: #f0f4ff;
    border-radius: 6px;
    padding: 8px 14px;
    margin: 4px 0;
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
st.title("🧮 Toán lớp 4 — AI Tutor")
st.caption("Chọn một chủ đề → AI sẽ tạo bài toán và giải thích thật dễ hiểu cho bé! 🌟")
st.divider()

# ── Topic selection ────────────────────────────────────────────────────────────
topic_map: dict[str, dict] = {t["name"]: t for t in TOPICS}

selected_name: str = st.selectbox(
    "📚 Chọn chủ đề bạn muốn luyện tập:",
    options=list(topic_map.keys()),
    index=0,
    help="Có 7 chủ đề toán lớp 4 để lựa chọn",
)
selected_topic = topic_map[selected_name]

# Hiển thị kiến thức sẽ được bao phủ
with st.expander("📖 Kiến thức bao phủ trong chủ đề này", expanded=False):
    for k in selected_topic["knowledge"]:
        st.markdown(f"- {k}")

st.divider()

# ── Action buttons ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    start_btn = st.button(
        "🚀 Bắt đầu học!",
        use_container_width=True,
        type="primary",
        disabled=False,
    )

with col2:
    has_results = bool(st.session_state.get("results"))
    retry_btn = st.button(
        "🔄 Tạo lại",
        use_container_width=True,
        disabled=not has_results,
    )

# ── Run pipeline ───────────────────────────────────────────────────────────────
if start_btn or retry_btn:
    st.session_state["results"] = None
    st.session_state["current_topic"] = selected_topic

    with st.spinner("🤖 AI đang tạo bài toán và lời giải... (khoảng 20–40 giây)"):
        try:
            orchestrator = Orchestrator()
            results = orchestrator.run(selected_topic)
            st.session_state["results"] = results
        except Exception as exc:
            st.error(
                f"😅 Ối, gặp sự cố rồi! Bạn thử lại nhé 🙂\n\n"
                f"Chi tiết lỗi: `{exc}`"
            )
            st.stop()

# ── Display results ────────────────────────────────────────────────────────────
results: list[dict] | None = st.session_state.get("results")

if results:
    current_topic = st.session_state.get("current_topic", {})

    st.success(
        f"✅ Đã tạo **{len(results)} bài toán** về chủ đề "
        f"**{current_topic.get('name', '')}**!"
    )
    st.divider()

    LEVEL_CONFIG = {
        "biết":       ("🟦 Biết",       "#1565c0", "#e3f2fd"),
        "hiểu":       ("🟧 Hiểu",       "#e65100", "#fff3e0"),
        "vận_dụng":   ("🟥 Vận dụng",   "#880e4f", "#fce4ec"),
    }

    for i, item in enumerate(results, start=1):
        problem: dict = item.get("problem", {})
        solution: dict = item.get("solution", {})
        level: str = problem.get("level", "biết")

        label, text_color, bg_color = LEVEL_CONFIG.get(
            level, ("🟦 Biết", "#1565c0", "#e3f2fd")
        )

        full_question = problem.get("question", "")
        expander_title = f"Bài {i} | {label} — {full_question}"

        with st.expander(expander_title, expanded=False):

            # --- Đề bài ---
            st.markdown(
                f'<div class="problem-card">'
                f'<strong>📝 Đề bài:</strong><br><br>'
                f'{problem.get("question", "")}'
                f'</div>',
                unsafe_allow_html=True,
            )

            if problem.get("hint"):
                st.caption(f"💡 **Gợi ý:** {problem['hint']}")

            st.markdown("---")

            # --- Lời giải ---
            if solution:
                if solution.get("read_problem"):
                    st.markdown(f"**🔍 Bài này hỏi gì?**")
                    st.markdown(f"> {solution['read_problem']}")

                if solution.get("thinking_direction"):
                    st.markdown(f"**🧭 Hướng giải:**")
                    st.markdown(f"*{solution['thinking_direction']}*")

                steps: list = solution.get("steps", [])
                if steps:
                    st.markdown("**📌 Các bước giải:**")
                    for step in steps:
                        st.markdown(
                            f'<div class="step-item">▶ {step}</div>',
                            unsafe_allow_html=True,
                        )

                if solution.get("answer"):
                    st.success(f"🎉 **Đáp án:** {solution['answer']}")

                if solution.get("explanation"):
                    st.markdown(
                        f"**🍭 Giải thích dễ hiểu hơn:**\n\n{solution['explanation']}"
                    )

                if solution.get("skill_note"):
                    st.info(f"🧠 **Kỹ năng tư duy học được:** {solution['skill_note']}")

            else:
                st.warning("⚠️ Không thể tạo lời giải cho bài này. Bạn thử lại nhé!")

    st.divider()
    st.markdown(
        "💪 **Cố lên!** Làm nhiều bài toán mỗi ngày, "
        "bé sẽ ngày càng giỏi hơn! ⭐"
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
elif not results:
    st.markdown(
        """
        ### Hướng dẫn sử dụng

        1. 📚 **Chọn chủ đề** bạn muốn ôn tập từ danh sách ở trên
        2. 🚀 Nhấn **"Bắt đầu học!"** và chờ AI tạo bài
        3. 📝 Đọc từng **đề bài**, thử tự giải trước
        4. 👁️ Mở xem **lời giải** để kiểm tra và học cách giải thích

        > 🌟 Mỗi lần tạo sẽ có bộ bài toán MỚI — bấm "Tạo lại" để luyện thêm!
        """
    )
