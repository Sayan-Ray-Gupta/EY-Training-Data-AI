from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import traceback

app = FastAPI()
visit_count = 0


@app.middleware("http")
async def count_visits(request: Request, call_next):
    global visit_count
    visit_count += 1
    count = visit_count
    print(f" Visit number: {count}")
    response = await call_next(request)
    return response


students = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Neha"}]


@app.get("/students")
def get_students():
    return students