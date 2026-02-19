"""
Streamlit UI for HR Support Chatbot with memory.
"""
import streamlit as st
from collections import deque
from hr_core import get_response
import time

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="HR Support Chatbot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding-top: 0;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 0.5rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #7b1fa2;
    }
    
    .message-content {
        flex: 1;
        line-height: 1.6;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #1976d2 0%, #7b1fa2 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Input section */
    .input-section {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Chat container */
    .chat-container {
        background-color: #fafafa;
        border-radius: 0.75rem;
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        min-height: 450px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1976d2;
    }
    
    .sidebar-section h3 {
        margin-top: 0;
        color: #1976d2;
    }
    
    /* Metric styling */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .metric-box {
        flex: 1;
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1976d2;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1565c0 !important;
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
    }
    
    /* Clear button */
    .clear-btn > button {
        background-color: #d32f2f !important;
        color: white !important;
    }
    
    .clear-btn > button:hover {
        background-color: #c62828 !important;
    }
    
    /* Loading spinner */
    .stSpinner > div > div {
        color: #1976d2;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------
if "memory" not in st.session_state:
    st.session_state.memory = deque(maxlen=10)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# -----------------------------------------
# HEADER SECTION
# -----------------------------------------
st.markdown("""
    <div class="header-container">
        <h1>💼 HR Support Chatbot</h1>
        <p>Your intelligent assistant for HR policies and company guidelines</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# MAIN LAYOUT
# -----------------------------------------
col1, col2 = st.columns([3, 1], gap="medium")

with col1:
    # Chat history display
    st.markdown("### 💬 Conversation History")
    
    chat_container = st.container(border=True)
    with chat_container:
        if not st.session_state.chat_history:
            st.info("👋 Start a conversation by asking a question about HR policies!")
        else:
            for i, msg in enumerate(st.session_state.chat_history):
                if msg["role"] == "user":
                    st.markdown(f"""
                        <div class="chat-message user-message">
                            <div class="message-content">
                                <b>You:</b><br>{msg['content']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="chat-message assistant-message">
                            <div class="message-content">
                                <b>🤖 HR Bot:</b><br>{msg['content']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

with col2:
    # Sidebar info metrics
    st.markdown("### 📊 Session Info")
    
    # Metrics display
    st.metric("Total Messages", len(st.session_state.chat_history))
    st.metric("Memory Exchanges", f"{len(st.session_state.memory)}/10")
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be specific with your questions
    - Ask about policies, benefits, leave
    - Mention departments if relevant
    - The bot uses conversation history for context
    """)

# -----------------------------------------
# INPUT SECTION
# -----------------------------------------
st.markdown("---")
st.markdown("### ❓ Ask Your Question")

col_input, col_btn = st.columns([4, 1], gap="small")

with col_input:
    user_input = st.text_input(
        "Your question:",
        placeholder="e.g., What is the annual leave policy? How do I request leave?",
        label_visibility="collapsed",
        key="user_input"
    )

with col_btn:
    submit_btn = st.button("Send", use_container_width=True, type="primary")

# -----------------------------------------
# PROCESS INPUT
# -----------------------------------------
if submit_btn and user_input.strip():
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    st.session_state.message_count += 1
    
    # Get response from chatbot with loading animation
    with st.spinner("🤔 HR Bot is thinking..."):
        try:
            response = get_response(user_input, st.session_state.memory)
            
            # Add assistant message to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Store in memory for context
            st.session_state.memory.append((user_input, response))
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Rerun to display new messages
    st.rerun()

# -----------------------------------------
# SIDEBAR
# -----------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Actions")

if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.memory = deque(maxlen=10)
    st.session_state.message_count = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.markdown("""
**HR Support Chatbot** uses AI to answer your HR questions instantly.

**Features:**
- 🧠 Conversation memory (last 10 exchanges)
- 📚 Company HR knowledge base
- ⚡ Instant responses
- 🔒 Privacy-focused

**How it works:**
1. Ask your HR question
2. Bot searches the knowledge base
3. Get instant, policy-aligned answers
""")

st.sidebar.markdown("---")
st.sidebar.caption("💼 Powered by LangChain & Google Generative AI")

