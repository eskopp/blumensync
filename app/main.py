import asyncio
import os
import random

from fastapi import FastAPI, Header, HTTPException
from starlette.responses import HTMLResponse, StreamingResponse

app = FastAPI()

SYNC_TOKEN = os.environ["SYNC_TOKEN"]

PAGE = """<!doctype html>
<title>blumensync</title>
<h1>blumensync</h1>
<p>Fake-Sync-Endpoint. Gibt alle 1-10 Sekunden eine Fortschrittszeile in 10%-Schritten aus, 80% der Laeufe erfolgreich, 20% brechen mit einem Fehler ab.</p>
<p>Aufruf per curl:</p>
<pre>curl -N -H "Authorization: Bearer &lt;TOKEN&gt;" https://dev.erik-skopp.de/blumen/sync</pre>
"""


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
    if authorization is None:
        return HTMLResponse(PAGE)
    if authorization != f"Bearer {SYNC_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return StreamingResponse(stream_generator(), media_type="text/plain")
