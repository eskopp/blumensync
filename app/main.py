import asyncio
import os
import random

from fastapi import FastAPI, Header, HTTPException
from starlette.responses import HTMLResponse, Response, StreamingResponse

app = FastAPI()

SYNC_TOKEN = os.environ["SYNC_TOKEN"]

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0f1117"/>
  <rect x="5" y="7" width="22" height="18" rx="2" fill="none" stroke="#5b8dee" stroke-width="2"/>
  <path d="M10 14l3 3-3 3" fill="none" stroke="#5b8dee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M16 20h6" stroke="#5b8dee" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

PAGE = """<!doctype html>
<title>blumensync</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<h1>blumensync</h1>
<p>Fake sync endpoint. Emits a progress line every 1-10 seconds in 10% steps. About 80% of runs succeed, 20% fail partway through. The last line is always "true" or "false".</p>
<p>Call it with curl:</p>
<pre>curl -N -H "Authorization: Bearer &lt;TOKEN&gt;" https://dev.erik-skopp.de/blumensync/sync</pre>
<p>Example successful run:</p>
<pre>10% - syncing...
20% - syncing...
30% - syncing...
40% - syncing...
50% - syncing...
60% - syncing...
70% - syncing...
80% - syncing...
90% - syncing...
100% - sync complete
true</pre>
<p>Example failed run:</p>
<pre>10% - syncing...
20% - syncing...
30% - ERROR: sync failed
false</pre>
"""


async def stream_generator():
    success = random.random() < 0.8
    stop_at = None if success else random.choice(range(10, 100, 10))

    for pct in range(10, 101, 10):
        await asyncio.sleep(random.uniform(1, 10))

        if not success and pct >= stop_at:
            yield f"{pct}% - ERROR: sync failed\n"
            yield "false\n"
            return

        yield f"{pct}% - syncing...\n"

    yield "100% - sync complete\n"
    yield "true\n"


@app.get("/favicon.svg")
async def favicon():
    return Response(FAVICON, media_type="image/svg+xml")


@app.get("/sync")
async def sync(authorization: str = Header(None)):
    if authorization is None:
        return HTMLResponse(PAGE)
    if authorization != f"Bearer {SYNC_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return StreamingResponse(stream_generator(), media_type="text/plain")
