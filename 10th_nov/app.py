import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Simple Chatbot",
    page_icon="🤖",
    layout="centered"
)

# API endpoint
API_URL = "http://localhost:8000/chat"

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 Simple Chatbot")
st.markdown("---")

# Description
st.markdown("""
**I can help you with:**
- Adding two numbers
- Telling today's date
- Reversing words
""")

st.markdown("---")

# Input section
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message:",
        placeholder="Type your message here... (e.g., 'add 5 and 3')",
        key="input"
    )
    submit_button = st.form_submit_button("Submit")

# Handle submission
if submit_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    # Call API
    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                json={"message": user_input},
                timeout=10
            )

            if response.status_code == 200:
                bot_response = response.json()["response"]
                st.session_state.messages.append({
                    "role": "bot",
                    "content": bot_response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            else:
                st.error(f"Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to the chatbot server. Please make sure the FastAPI server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

# Display chat history
st.markdown("---")
st.subheader("💬 Conversation")

if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.container():
                st.markdown(f"**You** ({msg['timestamp']})")
                st.info(msg["content"])
        else:
            with st.container():
                st.markdown(f"**Bot** ({msg['timestamp']})")
                st.success(msg["content"])
else:
    st.write("No messages yet. Start a conversation!")

# Clear chat button
if st.session_state.messages:
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This is a simple chatbot that can:")
    st.write("- ➕ Add two numbers")
    st.write("- 📅 Tell you today's date")
    st.write("- 🔄 Reverse words")

    st.markdown("---")
    st.subheader("Example queries:")
    st.code("add 10 and 20")
    st.code("what's today's date?")
    st.code("reverse python")

    st.markdown("---")
    st.caption("Built with FastAPI & Streamlit")