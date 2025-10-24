import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define a dynamic ChatPromptTemplate
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a summarizer assistant. summarize {topic} under 60 words and giving the important facts. You are also a master quiz creator who will generate 3 question on the basis of {topic}[/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()

#4. create a reusable chain (prompts -> model -> Output)
def generated_explaination(topic):
    chain = prompt | llm | parser
    response = chain.invoke({"topic": topic})
    return response

#5 Run dynamically for any topic

user_topic =input("Enter the topic to summarize and generate quiz : ").strip()
response = generated_explaination(user_topic)

print("\n --- Mistral Response ---")
print(response)

#6 log the prompts and output
os.makedirs("logs", exist_ok=True )
log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "user": user_topic,
    "response": response,
}

with open("logs/sequential_chain_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry))

print("\nResponse logged to logs/prompt_template_log.jsonl")
