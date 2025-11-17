from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re
import logging
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
PORT = int(os.getenv("PORT", 8000))

# Log loaded configuration (without exposing sensitive data)
logger = logging.getLogger(__name__)
logger.info(f"API Key loaded: {'Yes' if API_KEY else 'No'}")
logger.info(f"Base URL: {BASE_URL if BASE_URL else 'Not set'}")
logger.info(f"Server Port: {PORT}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: Status {response.status_code} - Time: {process_time:.2f}s")

    return response


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    timestamp: str


def extract_numbers(text: str):
    """Extract numbers from text"""
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(n) for n in numbers]


def process_message(message: str) -> str:
    """Process user message and return appropriate response"""
    msg_lower = message.lower().strip()

    # Greeting
    if any(greet in msg_lower for greet in ['hello', 'hi', 'hey']):
        return "Hello! I can help you with:\n- Adding two numbers (e.g., 'add 5 and 3')\n- Telling you today's date\n- Reversing words (e.g., 'reverse hello')\n\nWhat would you like to do?"

    # Date query
    elif any(word in msg_lower for word in ['date', 'today', 'day']):
        today = datetime.now()
        return f"Today's date is: {today.strftime('%B %d, %Y (%A)')}"

    # Addition
    elif any(word in msg_lower for word in ['add', 'sum', 'plus', '+']):
        numbers = extract_numbers(message)
        if len(numbers) >= 2:
            result = numbers[0] + numbers[1]
            return f"The sum of {numbers[0]} and {numbers[1]} is: {result}"
        else:
            return "Please provide two numbers to add. Example: 'add 5 and 3'"

    # Reverse word
    elif 'reverse' in msg_lower:
        # Extract word after 'reverse'
        words = message.split()
        try:
            reverse_idx = next(i for i, w in enumerate(words) if 'reverse' in w.lower())
            if reverse_idx + 1 < len(words):
                word_to_reverse = words[reverse_idx + 1]
                reversed_word = word_to_reverse[::-1]
                return f"The reverse of '{word_to_reverse}' is: '{reversed_word}'"
            else:
                return "Please provide a word to reverse. Example: 'reverse hello'"
        except:
            return "Please provide a word to reverse. Example: 'reverse hello'"

    # Help
    elif 'help' in msg_lower:
        return "I can help you with:\n- Adding two numbers: 'add 5 and 3'\n- Today's date: 'what is today's date?'\n- Reversing words: 'reverse hello'\n\nJust ask me anything!"

    # Default response
    else:
        return "I'm not sure how to help with that. Try:\n- 'add 10 and 20'\n- 'what's today's date?'\n- 'reverse python'\n- 'help' for more options"


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received message: {request.message}")

    response_text = process_message(request.message)

    logger.info(f"Generated response: {response_text[:50]}...")

    return ChatResponse(
        response=response_text,
        timestamp=datetime.now().isoformat()
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)