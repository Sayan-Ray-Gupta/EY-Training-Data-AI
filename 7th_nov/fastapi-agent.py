from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime
from pathlib import Path

load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

HISTORY_FILE = "qa-history.json"


class Prompt(BaseModel):
    query: str

    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


def load_history():
    """Load Q&A history from file"""
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_to_history(query, response):
    """Save Q&A to history file"""
    history = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response
    }
    history.append(entry)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


@app.post("/generate")
async def generate_response(prompt: Prompt):
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.query}
            ]
        )

        answer = response.choices[0].message.content

        # Save to history
        save_to_history(prompt.query, answer)

        return {"response": answer}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    """Retrieve Q&A history"""
    return {"history": load_history()}


@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the frontend HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Q&A Assistant</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }

            .header h1 {
                font-size: 28px;
                margin-bottom: 10px;
            }

            .header p {
                opacity: 0.9;
                font-size: 14px;
            }

            .content {
                padding: 30px;
            }

            .input-section {
                margin-bottom: 30px;
            }

            label {
                display: block;
                margin-bottom: 10px;
                font-weight: 600;
                color: #333;
            }

            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                min-height: 100px;
                transition: border-color 0.3s;
            }

            textarea:focus {
                outline: none;
                border-color: #667eea;
            }

            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                width: 100%;
            }

            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }

            button:active {
                transform: translateY(0);
            }

            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .response-section {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                display: none;
            }

            .response-section.visible {
                display: block;
            }

            .response-title {
                font-weight: 600;
                color: #667eea;
                margin-bottom: 15px;
                font-size: 18px;
            }

            .response-text {
                color: #333;
                line-height: 1.6;
                white-space: pre-wrap;
            }

            .error {
                background: #fee;
                border-left: 4px solid #f44;
                padding: 15px;
                border-radius: 4px;
                color: #c33;
                margin-top: 20px;
            }

            .loading {
                text-align: center;
                padding: 20px;
                color: #667eea;
                font-weight: 600;
            }

            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Q&A Assistant</h1>
                <p>Ask me anything and get intelligent responses</p>
            </div>

            <div class="content">
                <div class="input-section">
                    <label for="query">Your Question:</label>
                    <textarea 
                        id="query" 
                        placeholder="Type your question here..."
                        rows="4"
                    ></textarea>
                </div>

                <button id="submitBtn" onclick="askQuestion()">
                    Get Answer
                </button>

                <div id="loading" class="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Thinking...</p>
                </div>

                <div id="responseSection" class="response-section">
                    <div class="response-title">Answer:</div>
                    <div id="response" class="response-text"></div>
                </div>

                <div id="error" style="display: none;"></div>
            </div>
        </div>

        <script>
            async function askQuestion() {
                const query = document.getElementById('query').value;
                const submitBtn = document.getElementById('submitBtn');
                const loading = document.getElementById('loading');
                const responseSection = document.getElementById('responseSection');
                const responseDiv = document.getElementById('response');
                const errorDiv = document.getElementById('error');

                // Clear previous messages
                errorDiv.style.display = 'none';
                responseSection.classList.remove('visible');

                // Validate input
                if (!query.trim()) {
                    errorDiv.textContent = 'Please enter a question';
                    errorDiv.className = 'error';
                    errorDiv.style.display = 'block';
                    return;
                }

                // Show loading state
                submitBtn.disabled = true;
                loading.style.display = 'block';

                try {
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query: query })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.detail || 'Something went wrong');
                    }

                    // Display response
                    responseDiv.textContent = data.response;
                    responseSection.classList.add('visible');

                } catch (error) {
                    errorDiv.textContent = `Error: ${error.message}`;
                    errorDiv.className = 'error';
                    errorDiv.style.display = 'block';
                } finally {
                    submitBtn.disabled = false;
                    loading.style.display = 'none';
                }
            }

            // Allow Enter+Shift for submit
            document.getElementById('query').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.shiftKey) {
                    e.preventDefault();
                    askQuestion();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)