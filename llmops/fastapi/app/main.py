import logging
import os
import uuid
from typing import Any, Dict

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load configuration from environment variables
HF_API_URL = os.getenv("HF_API_URL")
HF_API_KEY = os.getenv("HF_API_KEY")

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def generate_uuid():
    return str(uuid.uuid4())


class TextPrompt(BaseModel):
    prompt: str


async def call_hf_inference_api(prompt: str, request_id: str) -> Dict[str, Any]:
    payload = {"inputs": prompt}
    logger.info(
        f"Request ID {request_id}: Calling Hugging Face Inference API with payload: {payload}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HF_API_URL}/generate", headers=headers, json=payload
        )
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(
            f"Request ID {request_id}: Error calling Hugging Face Inference API: {response.text}"
        )
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error calling Hugging Face Inference API: {response.text}",
        )


@app.post("/generate-text/", response_model=Dict[str, Any])
async def generate_text(
    prompt: TextPrompt, request: Request, request_id: str = Depends(generate_uuid)
) -> Dict[str, Any]:
    logger.info(
        f"Request ID {request_id}: Received request with prompt: {prompt.prompt}"
    )
    preprocessed_prompt = prompt.prompt  # Placeholder for actual pre-processing logic
    hf_response = await call_hf_inference_api(preprocessed_prompt, request_id)
    generated_text = hf_response[
        "generated_text"
    ]  # call_hf_inference_api returns a json response with the generated text
    logger.info(f"Request ID {request_id}: Generated text: {generated_text}")
    response = {"generated_text": generated_text, "request_id": request_id}
    return response
