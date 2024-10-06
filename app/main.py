from fastapi import FastAPI, Query, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"  # Use a more appropriate model
API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Set your Hugging Face API key in the .env

@app.get("/generate_article")
async def generate_article(question: str = Query(...)):
    # Remove quotes if present
    question = question.strip('"')

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not set")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # More specific prompt
    prompt = f"Write a detailed, informative article about the {question}. Cover its physical characteristics, significance in space exploration, and any interesting facts that people may not know."

    payload = {
        "inputs": prompt,
        "options": {"max_length": 400}  # Adjust length for more focused output
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        article = response.json()
        return {"article": article[0]['generated_text']}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate article")
