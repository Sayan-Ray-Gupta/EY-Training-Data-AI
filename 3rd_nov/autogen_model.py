import os
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()
llm_config = {"config_list": [{"model": "mistralai/mistral-7b-instruct", "base_url": "https://openrouter.ai/api/v1",
                               "api_key": os.getenv("OPENROUTER_API_KEY")}]}
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about TESLA.",
)