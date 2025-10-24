import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    st.error("OPENROUTER_API_KEY not found in .env file")
    st.stop()

# Initialize LangChain model pointing to OpenRouter
llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# Streamlit UI
st.title("Q&A with Large Language Model")
st.markdown("Ask any question and get a response from the AI assistant.")

# Initialize session state for conversation history (optional, for multi-turn conversations)
if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Assistant:** {msg['content']}")

# User input
user_input = st.text_input("Enter your question:", key="user_input")

if st.button("Submit"):
    if user_input.strip():
        # Add user message to history
        st.session_state.history.append({"role": "user", "content": user_input})

        # Prepare messages for the LLM
        messages = [
            SystemMessage(content="You are a helpful and concise AI assistant."),
            HumanMessage(content=user_input),  # Removed [INST] format as it's for Mistral, not Gemini
        ]

        try:
            # Invoke the model
            response = llm.invoke(messages)
            assistant_response = response.content.strip() or "(no content returned)"

            # Add assistant response to history
            st.session_state.history.append({"role": "assistant", "content": assistant_response})

            # Display the latest response
            st.write(f"**Assistant:** {assistant_response}")

            # Rerun to update the UI with history
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

# Button to clear history
if st.button("Clear Conversation"):
    st.session_state.history = []
    st.rerun()
