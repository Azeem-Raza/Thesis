import streamlit as st
from agent import process_query

# Set page config with dark theme
st.set_page_config(
    page_title="Mobile Retail Customer Support",
    page_icon="📱",
    layout="centered"
)

# Custom CSS with dark theme
st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: #e0e0e0;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1.2rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        box-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    .chat-message.user {
        background-color: #2979ff;
        color: #ffffff;
    }
    .chat-message.bot {
        background-color: #333333;
        color: #f0f0f0;
        border: 1px solid #444444;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 20px;
        background-color: rgba(255, 255, 255, 0.1);
    }
    .chat-message .content {
        flex-grow: 1;
    }
    .stButton>button {
        background-color: #2979ff;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565c0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .sample-query {
        margin-bottom: 0.5rem;
    }
    .header {
        padding: 1.5rem 0;
        text-align: center;
        margin-bottom: 2rem;
        background-color: #1e1e1e;
        border-bottom: 1px solid #333333;
        color: #f0f0f0;
    }
    .footer {
        padding: 1rem 0;
        text-align: center;
        margin-top: 2rem;
        color: #a0a0a0;
        font-size: 0.9rem;
        border-top: 1px solid #333333;
    }
    .user-input-container {
        display: flex;
        margin-bottom: 2rem;
    }
    .send-button {
        width: 80px;
    }
    .section-title {
        color: #f0f0f0;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #f0f0f0;
        border: 1px solid #444444;
    }
    .stTextInput>div>div>input::placeholder {
        color: #a0a0a0;
    }
    .stTextInput>label {
        color: #f0f0f0;
    }
    .stInfo {
        background-color: #333333;
        color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize query state for sample queries
if "query_to_use" not in st.session_state:
    st.session_state.query_to_use = None

# App header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("📱 Mobile Retail Customer Support")
st.markdown("""
Our AI assistant can help you find products, check availability, track orders, and answer questions about our mobile phones.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
if st.session_state.messages:
    for message in st.session_state.messages:
        with st.container():
            avatar = "👤" if message["role"] == "user" else "🤖"
            st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div class="avatar">
                    {avatar}
                </div>
                <div class="content">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("👋 Hello! How can I help you today? Ask me about our mobile phones or your orders.")

# User input area with send button
st.markdown('<div class="user-input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])

# Check if we have a sample query to use
if st.session_state.query_to_use:
    user_input = st.session_state.query_to_use
    # Reset this so it doesn't persist
    st.session_state.query_to_use = None 
else:
    # User input area
    with col1:
        user_input = st.text_input("Type your message here...", key="user_input", placeholder="Ask about phones, prices, availability, or order status...")

with col2:
    st.markdown('<div class="send-button">', unsafe_allow_html=True)
    send_button = st.button("Send")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Process the user's message when submitted
if send_button and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display "thinking" message
    with st.spinner("AI Assistant is thinking..."):
        # Process query through our agent
        response = process_query(user_input)
    
    # Add agent response to chat history
    st.session_state.messages.append({"role": "bot", "content": response})
    
    # Rerun to update the UI
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Sample queries section
st.markdown('<h3 class="section-title">Try asking about:</h3>', unsafe_allow_html=True)

sample_queries = [
    "Do you have the iPhone 15 Pro in stock?",
    "What's the price of the Samsung Galaxy S24 Ultra?",
    "Tell me about the Google Pixel 8 Pro features",
    "What's the status of my order ORD10001?",
    "When will my order ORD10003 arrive?"
]

col1, col2 = st.columns(2)
for i, query in enumerate(sample_queries):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f'<div class="sample-query">', unsafe_allow_html=True)
        if st.button(query, key=f"sample_{i}"):
            st.session_state.query_to_use = query
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Powered by LangChain, LangGraph and Groq LLM")
st.markdown('</div>', unsafe_allow_html=True) 