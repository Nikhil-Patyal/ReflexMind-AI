import streamlit as st
import time
from agent import run_agent

st.set_page_config(page_title="ReflexMind Pro", layout="wide")

# ---------------------------
# 🎨 CUSTOM UI
# ---------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
    color: #111827;
}

/* Tagline */
.tagline {
    text-align: center;
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 22px;
}

/* Sidebar text */
.sidebar-text {
    font-size: 14px;
    color: #374151;
    margin-bottom: 8px;
}

/* Glass Cards */
.card {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(10px);
    padding: 18px;
    border-radius: 14px;
    margin: 12px 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* Borders */
.strategy {
    border-left: 6px solid #3b82f6;
}

.initial {
    border-left: 6px solid #f59e0b;
}

.eval {
    border-left: 6px solid #ef4444;
}

.final {
    border-left: 6px solid #10b981;
}

/* Chat spacing */
.stChatMessage {
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("<div class='title'>ReflexMind</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='tagline'>Think • Evaluate • Improve</div>",
    unsafe_allow_html=True
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard")

st.sidebar.markdown(
    "<div class='sidebar-text'><b>Model:</b> LLaMA 3.1 (Groq)</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div class='sidebar-text'><b>Mode:</b> Adaptive AI</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🧠 Features")
st.sidebar.write("✔ Iterative Thinking")
st.sidebar.write("✔ Self Evaluation")
st.sidebar.write("✔ Memory")

# ---------------------------
# CLEAR CHAT
# ---------------------------
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat = []
    st.session_state.steps = []
    st.rerun()

# ---------------------------
# SESSION MEMORY
# ---------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "steps" not in st.session_state:
    st.session_state.steps = []

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🧠 Thinking Process"])

# ---------------------------
# TYPING EFFECT
# ---------------------------
def typing_effect(text):
    placeholder = st.empty()
    output = ""

    for char in text:
        output += char
        placeholder.markdown(output + "▌")
        time.sleep(0.002)

    placeholder.markdown(output)

# ---------------------------
# CHAT TAB
# ---------------------------
with tab1:

    # Show old chat
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask anything...")

    if user_input:

        # Save user message
        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        # Show user message
        with st.chat_message("user"):
            st.write(user_input)

        # Run AI
        with st.spinner("Thinking..."):
            steps, final = run_agent(user_input)

        # Save thinking steps
        st.session_state.steps = steps

        # Assistant response with typing
        with st.chat_message("assistant"):
            typing_effect(final)

        # Save assistant response
        st.session_state.chat.append({
            "role": "assistant",
            "content": final
        })

        # Download button
        st.download_button(
            "📥 Download Answer",
            final,
            file_name="reflexmind.txt"
        )

# ---------------------------
# THINKING TAB
# ---------------------------
with tab2:

    st.subheader("🧠 AI Thinking Process")

    if st.session_state.steps:

        for title, content in st.session_state.steps:

            # Dynamic card colors
            if "Strategy" in title:
                css = "strategy"

            elif "Initial" in title:
                css = "initial"

            elif "Evaluation" in title:
                css = "eval"

            else:
                css = "final"

            # Card UI
            st.markdown(f"""
            <div class="card {css}">

                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-bottom:10px;
                    color:#111827;
                ">
                    {title}
                </div>

                <div style="
                    line-height:1.8;
                    color:#374151;
                    font-size:15px;
                ">
                    {content}
                </div>

            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Run a query to see thinking process.")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
<div style='text-align:center;
            color:gray;
            margin-top:30px;
            font-size:13px;'>

Built with Reflexive AI Reasoning • ReflexMind AI

</div>
""", unsafe_allow_html=True)