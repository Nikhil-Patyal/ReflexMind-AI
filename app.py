import streamlit as st
import time
from agent import run_agent

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="ReflexMind AI",
    layout="wide"
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: #f5f7fb;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 5px;
}

/* Tagline */
.tagline {
    font-size: 15px;
    color: #6b7280;
    margin-bottom: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* Cards */
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Thinking Borders */
.strategy {
    border-left: 5px solid #3b82f6;
}

.initial {
    border-left: 5px solid #f59e0b;
}

.eval {
    border-left: 5px solid #ef4444;
}

.final {
    border-left: 5px solid #10b981;
}

/* Chat spacing */
.stChatMessage {
    padding-top: 10px;
    padding-bottom: 10px;
}

/* Divider */
.divider {
    border-top: 1px solid #e5e7eb;
    margin: 10px 0 18px 0;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="main-title">
🧠 ReflexMind AI
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tagline">
Think • Evaluate • Improve
</div>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard")

st.sidebar.markdown("""
### ⚙️ Settings
""")

selected_model = st.sidebar.selectbox(
    "Choose Model",
    [
        "llama-3.3-70b-versatile",
        "qwen/qwen3-32b"
    ]
)

st.sidebar.markdown("""
### 🧠 Features

✔ Iterative Thinking  
✔ Self Evaluation  
✔ Adaptive Reasoning  
✔ Memory
""")

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

        # Save user msg
        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        # Show user msg
        with st.chat_message("user"):

            st.write(user_input)

        # AI processing
        with st.spinner("Thinking..."):

            steps, final = run_agent(
                user_input,
                selected_model
            )

        # Save thinking
        st.session_state.steps = steps

        # Assistant response
        with st.chat_message("assistant"):

            typing_effect(final)

        # Save assistant msg
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

    st.markdown("""
    <div class="divider"></div>
    """, unsafe_allow_html=True)

    if st.session_state.steps:

        for title, content in st.session_state.steps:

            # Style choose
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

                time.sleep(0.3)

            # CLEAN CARD
            st.markdown(
                f"""
                <div class="card {css}">

                    <div style="
                        font-size:18px;
                        font-weight:600;
                        margin-bottom:12px;
                        color:#111827;
                    ">
                        {title}
                    </div>

                    <div style="
                        line-height:1.8;
                        color:#374151;
                        font-size:15px;
                        white-space: pre-wrap;
                    ">
                        {content}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info("Run a query to see the AI thinking process.")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
<br>

<div style="
text-align:center;
color:gray;
font-size:13px;
padding-bottom:10px;
">

Built with Reflexive AI Reasoning • ReflexMind AI

</div>
""", unsafe_allow_html=True)