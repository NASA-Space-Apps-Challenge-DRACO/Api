from fastapi import FastAPI, Query, HTTPException
import httpx
import os
import re
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
AI_API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
AI_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Set your Hugging Face API key in the .env

async def fetch_wikipedia_content(query: str):
    params = {
        "action": "query",
        "format": "json",
        "titles": query,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(WIKIPEDIA_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        page = next(iter(data["query"]["pages"].values()))
        return page.get("extract", "")
    return ""

async def fetch_ai_content(prompt: str):
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "max_length": 500,
            "temperature": 0.5
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(AI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        article = response.json()
        if article and isinstance(article, list) and 'generated_text' in article[0]:
            articleResponse = article[0]['generated_text'].strip()
            # Remove the prompt from the beginning of the articleResponse
            if articleResponse.startswith(prompt):
                articleResponse = articleResponse[len(prompt):].strip()
            return articleResponse
    raise HTTPException(status_code=response.status_code, detail="Failed to generate article")

@app.get("/generate_article")
async def generate_article(query: str = Query(...)):
    query = query.strip('"')

    # First, try to fetch content from Wikipedia
    wikipedia_content = await fetch_wikipedia_content(query)

    if wikipedia_content:
        return {
            "query": query,
            "article": wikipedia_content
        }

    # If no relevant content from Wikipedia, fetch from AI
    prompt = (
        f"Provide a detailed explanation or information strictly related to: {query} "
        "without any introductory or contextual information."
    )
    ai_response = await fetch_ai_content(prompt)

    return {
        "query": query,
        "article": ai_response
    }

# Run with: uvicorn main:app --reload
