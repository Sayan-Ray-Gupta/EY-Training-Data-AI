from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

#----------- SYNC ENDPOINT --------------
@app.get("/sync-task")
def sync_task():
    time.sleep(10)  #blocking
    return {"message": "Sync task completed"}


#------------Async Endpoint

@app.get("/async-task")
async def async_task():
    await asyncio.sleep(10)
    return {"message": "Async task completed after 5 seconds"}