from fastapi import FastAPI, Query, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Set your Hugging Face API key in the .env

@app.get("/generate_article")
async def generate_article(query: str = Query(...)):
    # Clean up the input
    query = query.strip('"')

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not set")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Create a focused prompt
    prompt = (
        f"Provide a detailed explanation or information strictly related to: {query} "
        "without any introductory or contextual information."
    )

    payload = {
        "inputs": prompt,
        "options": {
            "max_length": 1000,  # Limit length to maintain focus
            "temperature": 0.5
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        article = response.json()
        # Extract only the relevant text from the response
        if article and isinstance(article, list) and 'generated_text' in article[0]:
            articleResponse = article[0]['generated_text'].strip()
            # Remove the prompt from the beginning of the articleResponse
            if articleResponse.startswith(prompt):
                articleResponse = articleResponse[len(prompt):].strip()

            return {
                "query": query,
                "article": articleResponse
            }
        else:
            raise HTTPException(status_code=500, detail="Invalid response structure")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate article")

# Run with: uvicorn main:app --reload
