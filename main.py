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
)

# Pull the private address securely from Render's environment variables
TAILSCALE_TARGET = os.getenv("PRIVATE_TARGET", "https://fallback-placeholder.ts.net")

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_to_local(request: Request, path_name: str):
    url = f"{TAILSCALE_TARGET}/{path_name}"
    client_body = await request.body()
    client_headers = dict(request.headers)
    client_headers.pop("host", None)

    async with httpx.AsyncClient(verify=False, timeout=60.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                content=client_body,
                headers=client_headers,
                params=request.query_params
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Tunnel communication error: {exc}")
