# ============================================================
# Task-Priority-Classifier-Tool.py — Conversational Mistral Agent with Task Priority Classifier Tool
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

    # Handle Priority command
    if user_input.lower().startswith("priority"):
        try:
            task_text = " ".join(user_input.split()[1:]).strip()
            if not task_text:
                print("Agent: Please provide a task to classify. Example: priority Submit proposal by tonight")
                continue
            # Use LLM to classify priority based on keywords and context
            prompt = f"Classify the priority of the following task as HIGH, MEDIUM, or LOW based on urgency keywords (e.g., 'by tonight' is HIGH, 'buy snacks' is LOW). Respond in the format: 'Task “{task_text}” marked as [PRIORITY] priority.' Task: {task_text}"
            response = llm.invoke(prompt)
            classification = response.content.strip()
            print("Agent:", classification)
            memory.save_context({"input": user_input}, {"output": classification})
            continue
        except Exception as e:
            print("Agent: Could not classify priority:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
