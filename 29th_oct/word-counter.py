
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

    # Handle Count command
    if user_input.lower().startswith("count"):
        try:
            sentence = " ".join(user_input.split()[1:]).strip()
            if not sentence:
                print("Agent: Please provide a sentence to count. Example: count I am learning LangChain with Mistral.")
                continue
            word_count = len(sentence.split())
            print(f"Agent: Your sentence has {word_count} words.")
            memory.save_context({"input": user_input}, {"output": f"Your sentence has {word_count} words."})
            continue
        except Exception as e:
            print("Agent: Could not count words:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
