from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "FastAPI Encryption Backend"}

class EncryptRequest(BaseModel):
    text: str

def encrypt_data(data: str) -> str:
    return data[::-1]

@app.post("/encrypt")
def encrypt_endpoint(request: EncryptRequest):
    ciphertext = encrypt_data(request.text)
    return {"ciphertext": ciphertext}
