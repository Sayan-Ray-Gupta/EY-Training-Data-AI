# ============================================================
# AI-Productivity-Assistant.py — Conversational Mistral Agent with Multiple Tools
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
# 3. Initialize memory and notes storage
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
notes = []  # List to store personal notes


# ------------------------------------------------------------
# 4. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your AI Productivity Assistant ===")
print("Available commands: summarize, analyze, note, get notes, improve, priority")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Summarize command
    if user_input.lower().startswith("summarize"):
        try:
            text_to_summarize = " ".join(user_input.split()[1:]).strip()
            if not text_to_summarize:
                print("Agent: Please provide text to summarize. Example: summarize The meeting discussed cloud migration...")
                continue
            # Use LLM to generate summary
            prompt = f"Summarize the following passage concisely: {text_to_summarize}"
            response = llm.invoke(prompt)
            summary = response.content.strip()
            print("Agent:", summary)
            memory.save_context({"input": user_input}, {"output": summary})
            continue
        except Exception as e:
            print("Agent: Could not summarize:", e)
            continue

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
