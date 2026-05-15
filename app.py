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

html, body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
}

/* Tagline */
.tagline {
    text-align: center;
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 20px;
}

/* Sidebar */
.sidebar-text {
    font-size: 14px;
    color: #374151;
    margin-bottom: 6px;
}

/* Chat */
.stChatMessage {
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    padding: 18px;
    border-radius: 14px;
    margin: 14px 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    animation: fadeIn 0.4s ease-in-out;
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

/* Animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class='title'>
ReflexMind
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='tagline'>
Think • Evaluate • Improve
</div>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard")

st.sidebar.markdown("""
<div class='sidebar-text'>
<b>Mode:</b> Adaptive AI
</div>
""", unsafe_allow_html=True)

# ---------------------------
# MODEL SWITCH
# ---------------------------
st.sidebar.markdown("### ⚙️ Settings")

selected_model = st.sidebar.selectbox(
    "Choose Model",
    [
        "llama-3.3-70b-versatile",
        "qwen/qwen3-32b"
    ]
)

# ---------------------------
# FEATURES
# ---------------------------
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
# SESSION
# ---------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "steps" not in st.session_state:
    st.session_state.steps = []

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs([
    "💬 Chat",
    "🧠 Thinking Process"
])

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

    # Previous chats
    for msg in st.session_state.chat:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

    # Input
    user_input = st.chat_input("Ask anything...")

    if user_input:

        # Save user message
        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        # Show user
        with st.chat_message("user"):

            st.write(user_input)

        # AI Processing
        with st.spinner("Thinking..."):

            steps, final = run_agent(
                user_input,
                selected_model
            )

        # Save steps
        st.session_state.steps = steps

        # Assistant output
        with st.chat_message("assistant"):

            typing_effect(final)

        # Save AI message
        st.session_state.chat.append({
            "role": "assistant",
            "content": final
        })

        # Download
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

            # Style selection
            if "Strategy" in title:
                css = "strategy"

            elif "Initial" in title:
                css = "initial"

            elif "Evaluation" in title:
                css = "eval"

            else:
                css = "final"

            # Animation
            with st.spinner(f"{title}..."):

                time.sleep(0.4)

            # CLEAN HTML CARD
            st.markdown(f"""
            <div class="card {css}">

                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-bottom:10px;
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
<div style='
    text-align:center;
    color:gray;
    margin-top:30px;
    font-size:13px;
'>
Built with Reflexive AI Reasoning • ReflexMind AI
</div>
""", unsafe_allow_html=True)