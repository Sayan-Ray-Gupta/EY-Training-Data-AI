# ============================================================
# Multi-Agent Research System using LangChain
# Agents: Researcher, Summarizer, Notifier
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
    max_tokens=512,  # Increased for research and summary
    api_key=api_key,
    base_url=base_url,
)

# ------------------------------------------------------------
# 3. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# ------------------------------------------------------------
# 4. Define Agent Functions
# ------------------------------------------------------------
def researcher_agent(topic):
    """Agent to research a topic."""
    prompt = f"Research the following topic in detail: {topic}. Provide key facts, explanations, and insights."
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error in research: {e}"


def summarizer_agent(research_output):
    """Agent to summarize the research output."""
    prompt = f"Summarize the following research concisely: {research_output}"
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error in summarization: {e}"


def notifier_agent(summary_output, filename="summary.txt"):
    """Agent to notify by writing the summary to a text file."""
    try:
        with open(filename, "w") as f:
            f.write(summary_output)
        return f"Summary saved to {filename}."
    except Exception as e:
        return f"Error in notifying: {e}"


# ------------------------------------------------------------
# 5. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Multi-Agent Research System ===")
print("Available commands: research <topic>, history")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    # Handle Research command (triggers the multi-agent chain)
    if user_input.lower().startswith("research"):
        try:
            topic = " ".join(user_input.split()[1:]).strip()
            if not topic:
                print("Agent: Please provide a topic to research. Example: research artificial intelligence")
                continue

            # Step 1: Researcher Agent
            research_output = researcher_agent(topic)
            print("Researcher Agent: Research completed.")

            # Step 2: Summarizer Agent
            summary_output = summarizer_agent(research_output)
            print("Summarizer Agent: Summary created.")

            # Step 3: Notifier Agent
            notify_output = notifier_agent(summary_output)
            print("Notifier Agent:", notify_output)

            # Overall output
            final_output = f"Research on '{topic}' completed. {notify_output}"
            print("Agent:", final_output)

            # Save to memory
            memory.save_context({"input": user_input}, {"output": final_output})
            continue
        except Exception as e:
            print("Agent: Error in research process:", e)
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

    # Default: use LLM for general conversation
    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)
