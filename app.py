
import streamlit as st
from assistant import get_support_response

st.set_page_config(
    page_title="ShopAssist AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: #101828;
    }

    [data-testid="stSidebar"] * {
        color: #f2f4f7;
    }

    .hero {
        background: linear-gradient(120deg, #182848, #355c9a);
        color: white;
        padding: 28px;
        border-radius: 18px;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e0eaff;
        font-size: 16px;
        margin-bottom: 0;
    }

    .info-card {
        background: white;
        border: 1px solid #e5eaf2;
        border-radius: 14px;
        padding: 18px;
        min-height: 112px;
    }

    .info-card h4 {
        color: #475467;
        font-size: 14px;
        margin: 0 0 8px 0;
    }

    .info-card p {
        color: #182848;
        font-size: 20px;
        font-weight: 700;
        margin: 0;
    }

    div[data-testid="stChatMessage"] {
        background: white;
        border: 1px solid #e8edf5;
        border-radius: 14px;
        padding: 14px;
    }

    .small-note {
        color: #667085;
        font-size: 13px;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🛍️ ShopAssist AI")
    st.caption("CUSTOMER SUPPORT WORKSPACE")
    st.divider()

    st.markdown("### What I can help with")
    st.markdown(
        """
        📦 Order tracking

        🚚 Delivery information

        💳 Refund eligibility

        💬 Customer questions
        """
    )

    st.divider()
    st.markdown("### Try a sample question")

    if st.button("📦 Track ORD1001", use_container_width=True):
        st.session_state.pending_question = (
            "Please track order ORD1001."
        )

    if st.button("💳 Check ORD1002 refund", use_container_width=True):
        st.session_state.pending_question = (
            "Is order ORD1002 eligible for a refund?"
        )

    if st.button("🔎 Find ORD9999", use_container_width=True):
        st.session_state.pending_question = (
            "Please check order ORD9999."
        )

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

    st.caption("Portfolio project • Demo order data")

# ---------- Main page ----------
st.markdown(
    """
    <div class="hero">
        <h1>Customer Support, Simplified.</h1>
        <p>
            Your AI shopping assistant for order updates,
            delivery questions and refund eligibility.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Summary cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h4>📦 Order Support</h4>
            <p>Order tracking</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h4>🚚 Delivery Help</h4>
            <p>Delivery updates</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <h4>💳 Refund Support</h4>
            <p>Eligibility checks</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### 💬 Chat with your assistant")
st.caption(
    "Ask a question below, or choose a sample question from the sidebar."
)

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            "Hi! 👋 I'm ShopAssist AI. "
            "I can help you check an order or its refund eligibility. "
            "What can I help you with today?"
        )

# Display conversation history
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Read either a sidebar sample question or normal chat input
pending_question = st.session_state.pop("pending_question", None)
chat_question = st.chat_input("Ask about your order or refund...")

question = pending_question or chat_question

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Checking your request..."):
            try:
                answer = get_support_response(question)
            except Exception as error:
                answer = (
                    "Sorry, I couldn't process that request right now. "
                    "Please try again in a moment.\n\n"
                    f"Technical details: `{str(error)[:300]}`"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.divider()
st.markdown(
    '<p class="small-note">Demo environment: orders and refund '
    'eligibility use sample data. No real payments or refunds are processed.</p>',
    unsafe_allow_html=True,
)
