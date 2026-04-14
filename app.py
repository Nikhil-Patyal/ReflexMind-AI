import streamlit as st
import time
from agent import run_agent

st.set_page_config(page_title="ReflexMind AI", layout="wide")

# ---------------------------
# 🎨 CHATGPT STYLE UI
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background: #0b0f19;
    color: white;
}

/* Chat bubbles */
.user-msg {
    background: #1f2937;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.bot-msg {
    background: #111827;
    padding: 14px 16px;
    border-radius: 12px;
    margin: 8px 0;
}

/* Title */
.title {
    font-size: 36px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown("<div class='title'>🧠 ReflexMind AI</div>", unsafe_allow_html=True)

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
tab1, tab2 = st.tabs(["💬 Chat", "🧠 Thinking"])

# ---------------------------
# TYPING EFFECT
# ---------------------------
def typing_effect(text):
    placeholder = st.empty()
    output = ""

    for char in text:
        output += char
        placeholder.markdown(f"<div class='bot-msg'>{output}</div>", unsafe_allow_html=True)
        time.sleep(0.002)

# ---------------------------
# CHAT TAB
# ---------------------------
with tab1:

    # Show chat history
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask anything...")

    if user_input:

        # Save user message
        st.session_state.chat.append({"role": "user", "content": user_input})

        st.markdown(f"<div class='user-msg'>{user_input}</div>", unsafe_allow_html=True)

        # Run agent
        with st.spinner("Thinking..."):
            steps, final = run_agent(user_input)

        st.session_state.steps = steps

        # Typing animation
        typing_effect(final)

        # Save assistant response
        st.session_state.chat.append({
            "role": "assistant",
            "content": final
        })

# ---------------------------
# THINKING TAB
# ---------------------------
with tab2:

    st.subheader("🧠 AI Thinking Process")

    if st.session_state.steps:

        for title, content in st.session_state.steps:

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                padding: 16px;
                border-radius: 12px;
                margin-bottom: 12px;
                border-left: 5px solid #3b82f6;
            ">
            <b>{title}</b><br><br>
            {content}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Ask something to see thinking process.")