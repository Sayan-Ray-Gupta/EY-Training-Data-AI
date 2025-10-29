
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
# 3. Initialize memory and notes storage
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
notes = []  # List to store personal notes


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

    # Handle Note command
    if user_input.lower().startswith("note"):
        try:
            note_text = " ".join(user_input.split()[1:]).strip()
            if not note_text:
                print("Agent: Please provide a note to remember. Example: note Remember to email the project report tomorrow.")
                continue
            notes.append(note_text)
            print(f"Agent: Noted: “{note_text}”")
            memory.save_context({"input": user_input}, {"output": f"Noted: “{note_text}”"})
            continue
        except Exception as e:
            print("Agent: Could not save note:", e)
            continue

    # Handle Get notes command
    if user_input.lower() == "get notes":
        try:
            if not notes:
                print("Agent: You have no notes stored.")
            else:
                note_list = "; ".join([f"“{note}”" for note in notes])
                print(f"Agent: You currently have {len(notes)} note(s): {note_list}")
            memory.save_context({"input": user_input}, {"output": f"You currently have {len(notes)} note(s): {note_list}" if notes else "You have no notes stored."})
            continue
        except Exception as e:
            print("Agent: Could not retrieve notes:", e)
            continue

    # Default: use LLM
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
