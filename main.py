from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Set PRIVATE_TARGET="https://laptop-setup.taild88315.ts.net" in Render Environment Variables
TAILSCALE_TARGET = os.getenv("PRIVATE_TARGET", "https://laptop-setup.taild88315.ts.net").rstrip("/")

EXCLUDED_REQ_HEADERS = {"host", "content-length", "accept-encoding", "connection"}
EXCLUDED_RESP_HEADERS = {"content-encoding", "content-length", "transfer-encoding", "connection"}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
async def proxy_to_local(request: Request, path_name: str):
    if request.method == "HEAD":
        return Response(status_code=200)

    url = f"{TAILSCALE_TARGET}/{path_name}"
    client_body = await request.body()
    
    req_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_REQ_HEADERS
    }

    async with httpx.AsyncClient(verify=False, timeout=60.0) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                content=client_body,
                headers=req_headers,
                params=request.query_params,
            )
            resp_headers = {
                k: v for k, v in resp.headers.items()
                if k.lower() not in EXCLUDED_RESP_HEADERS
            }
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=resp_headers,
                media_type=resp.headers.get("content-type"),
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Bad Gateway - Local node unreachable: {exc}")
