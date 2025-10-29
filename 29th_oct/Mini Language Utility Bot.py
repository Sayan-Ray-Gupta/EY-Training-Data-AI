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
print("Available commands: count, reverse, define, upper, lower, repeat, history")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Count command
    if user_input.lower().startswith("count"):
        try:
            sentence = " ".join(user_input.split()[1:]).strip()
            if not sentence:
                print("Agent: Please provide a sentence to count. Example: count I am learning LangChain with Mistral.")
                continue
            word_count = len(sentence.split())
            output = f"Your sentence has {word_count} words."
            print("Agent:", output)
            memory.save_context({"input": user_input}, {"output": output})
            continue
        except Exception as e:
            print("Agent: Could not count words:", e)
            continue

    # Handle Reverse command
    if user_input.lower().startswith("reverse"):
        try:
            text_to_reverse = " ".join(user_input.split()[1:]).strip()
            if not text_to_reverse:
                print("Agent: Please provide text to reverse. Example: reverse LangChain is fun to learn")
                continue
            reversed_text = " ".join(text_to_reverse.split()[::-1])
            print("Agent:", reversed_text)
            memory.save_context({"input": user_input}, {"output": reversed_text})
            continue
        except Exception as e:
            print("Agent: Could not reverse text:", e)
            continue

    # Handle Define command
    if user_input.lower().startswith("define"):
        try:
            word = " ".join(user_input.split()[1:]).strip()
            if not word:
                print("Agent: Please provide a word to define. Example: define curious")
                continue
            # Use LLM to provide definition or synonym
            prompt = f"Provide a short definition or synonym for the word '{word}'. Respond in the format: '{word.capitalize()} means [definition or synonym].'"
            response = llm.invoke(prompt)
            definition = response.content.strip()
            print("Agent:", definition)
            memory.save_context({"input": user_input}, {"output": definition})
            continue
        except Exception as e:
            print("Agent: Could not define word:", e)
            continue

    # Handle Upper command
    if user_input.lower().startswith("upper"):
        try:
            text_to_upper = " ".join(user_input.split()[1:]).strip()
            if not text_to_upper:
                print("Agent: Please provide text to convert to uppercase. Example: upper I like learning AI.")
                continue
            upper_text = text_to_upper.upper()
            print("Agent:", upper_text)
            memory.save_context({"input": user_input}, {"output": upper_text})
            continue
        except Exception as e:
            print("Agent: Could not convert to uppercase:", e)
            continue

    # Handle Lower command
    if user_input.lower().startswith("lower"):
        try:
            text_to_lower = " ".join(user_input.split()[1:]).strip()
            if not text_to_lower:
                print("Agent: Please provide text to convert to lowercase. Example: lower THIS IS AMAZING!")
                continue
            lower_text = text_to_lower.lower()
            print("Agent:", lower_text)
            memory.save_context({"input": user_input}, {"output": lower_text})
            continue
        except Exception as e:
            print("Agent: Could not convert to lowercase:", e)
            continue

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
