import os
from typing import Any, Dict

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Load configuration from environment variables
HF_API_URL = os.getenv("HF_API_URL")
HF_API_KEY = os.getenv("HF_API_KEY")

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


class TextPrompt(BaseModel):
    prompt: str


async def call_hf_inference_api(prompt: str) -> Dict[str, Any]:
    payload = {"inputs": prompt}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HF_API_URL}/generate", headers=headers, json=payload
        )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error calling Hugging Face Inference API: {response.text}",
        )


@app.post("/generate-text/", response_model=Dict[str, Any])
async def generate_text(prompt: TextPrompt) -> Dict[str, Any]:
    preprocessed_prompt = prompt.prompt  # Placeholder for actual pre-processing logic
    hf_response = await call_hf_inference_api(preprocessed_prompt)
    generated_text = hf_response[
        "generated_text"
    ]  # call_hf_inference_api returns a json response with the generated text
    return {"generated_text": generated_text}
