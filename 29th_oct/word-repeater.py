# ============================================================
# Word-Repeater-Tool.py — Conversational Mistral Agent with Word Repeater Tool
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

    # Handle Repeat command
    if user_input.lower().startswith("repeat"):
        try:
            parts = user_input.split()
            if len(parts) < 3:
                print("Agent: Please provide a word and a number. Example: repeat hello 3")
                continue
            word = parts[1]
            count = int(parts[2])
            if count <= 0:
                print("Agent: Please provide a positive number.")
                continue
            repeated_text = " ".join([word] * count)
            print("Agent:", repeated_text)
            memory.save_context({"input": user_input}, {"output": repeated_text})
            continue
        except ValueError:
            print("Agent: Please provide a valid number. Example: repeat hello 3")
            continue
        except Exception as e:
            print("Agent: Could not repeat word:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
