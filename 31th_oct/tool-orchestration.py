# ============================================================
# Text-Processing-Bot.py — Conversational Mistral Agent with Multiple Text Tools
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
print("\n=== Start chatting with your Text Processing Bot ===")
print("Available commands: length, vowels, sort, history")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Length command
    if user_input.lower().startswith("length"):
        try:
            text = " ".join(user_input.split()[1:]).strip()
            if not text:
                print("Agent: Please provide text to measure length. Example: length Hello world")
                continue
            char_length = len(text)
            output = f"Your text has {char_length} characters."
            print("Agent:", output)
            memory.save_context({"input": user_input}, {"output": output})
            continue
        except Exception as e:
            print("Agent: Could not measure length:", e)
            continue

    # Handle Vowels command
    if user_input.lower().startswith("vowels"):
        try:
            text = " ".join(user_input.split()[1:]).strip()
            if not text:
                print("Agent: Please provide text to count vowels. Example: vowels Hello world")
                continue
            vowels = "aeiouAEIOU"
            vowel_count = sum(1 for char in text if char in vowels)
            output = f"Your text has {vowel_count} vowels."
            print("Agent:", output)
            memory.save_context({"input": user_input}, {"output": output})
            continue
        except Exception as e:
            print("Agent: Could not count vowels:", e)
            continue

    # Handle Sort command
    if user_input.lower().startswith("sort"):
        try:
            text_to_sort = " ".join(user_input.split()[1:]).strip()
            if not text_to_sort:
                print("Agent: Please provide text to sort. Example: sort zebra apple banana")
                continue
            sorted_words = " ".join(sorted(text_to_sort.split()))
            print("Agent:", sorted_words)
            memory.save_context({"input": user_input}, {"output": sorted_words})
            continue
        except Exception as e:
            print("Agent: Could not sort text:", e)
            continue

    # Handle History command
    if user_input.lower() == "history":
        try:
            messages = memory.load_memory_variables({}).get("chat_history", [])
            if not messages:
                print("Agent: No history available.")
            else:
                print("Agent: Conversation History:")
                for msg in messages:
                    if hasattr(msg, 'type') and msg.type == 'human':
                        print(f"You: {msg.content}")
                    elif hasattr(msg, 'type') and msg.type == 'ai':
                        print(f"Agent: {msg.content}")
            # Note: We don't save history command to memory to avoid recursion
            continue
        except Exception as e:
            print("Agent: Could not retrieve history:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
