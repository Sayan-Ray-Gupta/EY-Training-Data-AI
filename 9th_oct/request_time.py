import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time
import traceback


app = FastAPI()

# ---------------- SETUP STRUCTURED LOGGING ----------------
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

@app.middleware("http")
async def time_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    duration = time.time() - start_time
    logging.info(f"Duration: {duration: 4f} seconds")
    response.headers['duration'] = str(duration)
    return response


students = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Neha"}]


@app.get("/students")
async def get_students():
    logging.info("Fetching students from database....")
    await asyncio.sleep(5)
    return students
