# ============================================================
# Text-Improver-Tool.py — Conversational Mistral Agent with Text Improver Tool
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


# ------------------------------------------------------------
# 2. Initialize the Mistral model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)


# ------------------------------------------------------------
# 3. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# ------------------------------------------------------------
# 4. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Improve command
    if user_input.lower().startswith("improve"):
        try:
            text_to_improve = " ".join(user_input.split()[1:]).strip()
            if not text_to_improve:
                print("Agent: Please provide text to improve. Example: improve This report is kind of messy and confusing.")
                continue
            # Use LLM to rewrite text
            prompt = f"Rewrite the following text to make it clearer and more professional: {text_to_improve}"
            response = llm.invoke(prompt)
            improved_text = response.content.strip()
            print("Agent:", improved_text)
            memory.save_context({"input": user_input}, {"output": improved_text})
            continue
        except Exception as e:
            print("Agent: Could not improve text:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
