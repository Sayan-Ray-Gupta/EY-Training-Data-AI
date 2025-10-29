# ============================================================
# Sentiment-Analyzer-Tool.py — Conversational Mistral Agent with Sentiment Analyzer Tool
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

    # Handle Analyze command
    if user_input.lower().startswith("analyze"):
        try:
            text_to_analyze = " ".join(user_input.split()[1:]).strip()
            if not text_to_analyze:
                print("Agent: Please provide text to analyze. Example: analyze I feel frustrated about work today.")
                continue
            # Use LLM to detect sentiment
            prompt = f"Analyze the sentiment of the following text and respond in the format: 'The sentiment is [positive/neutral/negative] — [brief explanation].' Text: {text_to_analyze}"
            response = llm.invoke(prompt)
            analysis = response.content.strip()
            print("Agent:", analysis)
            memory.save_context({"input": user_input}, {"output": analysis})
            continue
        except Exception as e:
            print("Agent: Could not analyze sentiment:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
