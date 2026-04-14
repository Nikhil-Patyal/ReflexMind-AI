import streamlit as st
import time
from agent import run_agent

st.set_page_config(page_title="ReflexMind Pro", layout="wide")

# ---------------------------
# 🎨 CUSTOM UI (UNCHANGED)
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

/* Glass Cards */
.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    padding: 16px;
    border-radius: 14px;
    margin: 10px 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    transition: 0.2s;
}

.card:hover {
    transform: scale(1.02);
}

/* Borders */
.strategy { border-left: 6px solid #3b82f6; }
.initial { border-left: 6px solid #f59e0b; }
.eval { border-left: 6px solid #ef4444; }
.final { border-left: 6px solid #10b981; }

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("<div class='title'>ReflexMind</div>", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR DASHBOARD
# ---------------------------
st.sidebar.title("📊 Dashboard")
st.sidebar.metric("Model", "Groq LLaMA")
st.sidebar.metric("Mode", "Adaptive AI")

st.sidebar.markdown("### 🧠 Features")
st.sidebar.write("✔ Iterative Thinking")
st.sidebar.write("✔ Self Evaluation")
st.sidebar.write("✔ Memory")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat = []

# ---------------------------
# SESSION MEMORY
# ---------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🧠 Thinking Process"])

# ---------------------------
# 🔥 TYPING EFFECT (ONLY ADDITION)
# ---------------------------
def typing_effect(text):
    placeholder = st.empty()
    output = ""

    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(0.002)

# ---------------------------
# CHAT TAB
# ---------------------------
with tab1:

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask anything...")

    if user_input:

        st.session_state.chat.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        history = "\n".join([m["content"] for m in st.session_state.chat])

        with st.spinner("Thinking..."):
            steps, final = run_agent(user_input, history)

        st.session_state.steps = steps

        # ✅ ONLY CHANGE → typing effect here
        with st.chat_message("assistant"):
            typing_effect(final)

        st.session_state.chat.append({
            "role": "assistant",
            "content": final
        })

        # Download
        st.download_button("📥 Download Answer", final, file_name="reflexmind.txt")

# ---------------------------
# THINKING TAB
# ---------------------------
with tab2:

    st.subheader("🧠 AI Thinking Process")

    if "steps" in st.session_state:

        for title, content in st.session_state.steps:

            if "Strategy" in title:
                css = "strategy"
            elif "Initial" in title:
                css = "initial"
            elif "Evaluation" in title:
                css = "eval"
            else:
                css = "final"

            st.markdown(f"""
            <div class="card {css}">
            <b>{title}</b><br>{content}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Run a query to see thinking process.")