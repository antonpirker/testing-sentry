import json
import gzip
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils import format_envelope_item


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Sentry Test Server. Use DSN http://123@localhost:9999/0 in your SDK."
    }


@app.post("/api/0/envelope/")
async def envelope(request: Request):
    print("\n~~~~~~~~~~~~~~~~~ Envelope Received ~~~~~~~~~~~~~~~~~")

    print("HTTP Tracing Headers:")
    print(f"  sentry-trace: {request.headers.get('sentry-trace')}")
    print(f"  baggage: {request.headers.get('baggage')}")
    
    raw_body = await request.body()

    try:
        body = gzip.decompress(raw_body).decode('utf-8')
    except:
        # If decompression fails, assume it's plain text
        body = raw_body.decode('utf-8')
    
    lines = body.split('\n')
    
    print("Envelope Header:")
    envelope_header = json.loads(lines[0])
    print(f"  {envelope_header}")
    
    current_line = 1
    while current_line < len(lines):
        if not lines[current_line].strip():
            current_line += 1
            continue
            
        # Parse item header
        item_header = json.loads(lines[current_line])
        current_line += 1

        # If we have a length in header, we can get the payload directly
        if 'length' in item_header:
            payload = lines[current_line]

            print("Envelope Item Header:")
            print(f"  {item_header}")

            print("Envelope Item Payload:")
            print(format_envelope_item(payload))

            current_line += 1
    
    return JSONResponse(content={}, status_code=200)
