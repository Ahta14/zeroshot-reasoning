from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import ollama
import json
import random
import numpy as np
from utils.prompts import get_prompt_template, get_schema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data["question"]
    strategy = data.get("strategy", "got")
    full_prompt = get_prompt_template(strategy, question)
    schema = get_schema(strategy)

    def generate():
        stream = ollama.chat(
            model="gemma3:4b",
            messages=[{"role": "user", "content": full_prompt}],
            options={"schema": schema},
            stream=True
        )
        for chunk in stream:
            content = chunk['message']['content']
            print(f"{content}")
            yield content

    return StreamingResponse(generate(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
