from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

# Pulled strictly from Render Environment Variables — zero local details in source code
PRIVATE_TARGET = os.getenv("PRIVATE_TARGET", "").rstrip("/")

EXCLUDED_REQ_HEADERS = {"host", "content-length", "accept-encoding", "connection"}
EXCLUDED_RESP_HEADERS = {"content-encoding", "content-length", "transfer-encoding", "connection"}

http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    http_client = httpx.AsyncClient(
        verify=False,
        timeout=httpx.Timeout(60.0, connect=15.0),
        follow_redirects=True,
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
    )
    yield
    await http_client.aclose()


app = FastAPI(title="Secure Edge Proxy", docs_url=None, redoc_url=None, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Original-Filename"],
)


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
async def proxy_to_local(request: Request, path_name: str):
    if request.method == "HEAD":
        return Response(status_code=200)

    if not PRIVATE_TARGET:
        raise HTTPException(
            status_code=503,
            detail="Gateway target not configured. Set PRIVATE_TARGET in environment variables.",
        )

    target_url = f"{PRIVATE_TARGET}/{path_name}"
    client_body = await request.body()

    req_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_REQ_HEADERS
    }

    try:
        resp = await http_client.request(
            method=request.method,
            url=target_url,
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
        raise HTTPException(status_code=502, detail=f"Tunnel gateway unreachable: {exc}")
