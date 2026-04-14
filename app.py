import streamlit as st
from agent import run_agent

st.set_page_config(page_title="ReflexMind", layout="wide")

# ---------------------------
# 🎨 UI STYLE (IMPROVED)
# ---------------------------
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Title */
.title-main {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
    color: #e2e8f0;
}

.title-sub {
    text-align: center;
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 14px;
    border-radius: 10px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown("""
<div class="title-main">ReflexMind</div>
<div class="title-sub">Online AI Problem Solver</div>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard")
st.sidebar.write("Model: LLaMA 3.1")
st.sidebar.write("Mode: Online AI")

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
# CHAT
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
            st.markdown(f"""
            <div class="card">
            <b>{title}</b><br>{content}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Run a query to see thinking process.")