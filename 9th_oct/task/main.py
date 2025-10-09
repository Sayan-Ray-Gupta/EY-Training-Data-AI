from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Sample data: 5 students
students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "Diana"},
    {"id": 5, "name": "Evan"}
]

@app.get("/api/students")
async def get_students():
    return students

# Serve static files from the 'static' folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")