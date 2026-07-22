import asyncio
import os
import random

from fastapi import FastAPI, Header, HTTPException
from starlette.responses import StreamingResponse

app = FastAPI()

SYNC_TOKEN = os.environ["SYNC_TOKEN"]


async def stream_generator():
    success = random.random() < 0.8
    stop_at = None if success else random.choice(range(10, 100, 10))

    for pct in range(10, 101, 10):
        await asyncio.sleep(random.uniform(1, 10))

        if not success and pct >= stop_at:
            yield f"{pct}% - ERROR: sync failed\n"
            return

        yield f"{pct}% - syncing factsheet images...\n"

    yield "100% - sync complete\n"


@app.get("/sync")
async def sync(authorization: str = Header(None)):
    if authorization != f"Bearer {SYNC_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return StreamingResponse(stream_generator(), media_type="text/plain")
