import streamlit as st
from agent import run_agent

st.set_page_config(page_title="ReflexMind", layout="wide")

# ---------------------------
# UI STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.title-main {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.title-sub {
    text-align: center;
    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 25px;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 14px;
    margin: 10px 0;
}

.strategy { border-left: 6px solid #3b82f6; }
.initial { border-left: 6px solid #f59e0b; }
.eval { border-left: 6px solid #ef4444; }
.final { border-left: 6px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown("""
<div class="title-main">ReflexMind</div>
<div class="title-sub">Adaptive Problem-Solving AI Agent</div>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard")
st.sidebar.metric("Model", "Mixtral (Groq)")
st.sidebar.metric("Mode", "Online AI")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat = []

# ---------------------------
# SESSION
# ---------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🧠 Thinking"])

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

        with st.spinner("Thinking..."):
            steps, final = run_agent(user_input)

        st.session_state.steps = steps

        with st.chat_message("assistant"):
            st.write(final)

        st.session_state.chat.append({
            "role": "assistant",
            "content": final
        })

# ---------------------------
# THINKING TAB
# ---------------------------
with tab2:
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