import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Hugging Face Inference API URL for your model
HF_API_URL = "https://api-inference.huggingface.co/models/YOUR_MODEL_NAME"
# Replace YOUR_HF_API_KEY with your actual Hugging Face API key
headers = {"Authorization": f"Bearer YOUR_HF_API_KEY"}


def call_hf_inference_api(prompt: str):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error calling Hugging Face Inference API",
        )


@app.post("/generate-text/")
async def generate_text(prompt: str):
    # Pre-processing (if needed)
    preprocessed_prompt = prompt  # Placeholder for actual pre-processing logic

    # Call Hugging Face Inference API
    hf_response = call_hf_inference_api(preprocessed_prompt)

    # Post-processing (if needed)
    generated_text = hf_response[0][
        "generated_text"
    ]  # Placeholder for actual post-processing logic

    return {"generated_text": generated_text}
