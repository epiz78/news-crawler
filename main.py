from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class LinkRequest(BaseModel):
    url: str

@app.post("/crawl")
async def crawl_news(data: LinkRequest):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(data.url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        return {"error": "Fetch failed"}

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string.strip() if soup.title else "No Title"
    content_meta = soup.find('meta', {'name': 'description'})
    content = content_meta['content'].strip() if content_meta else "No Content"
    image_meta = soup.find('meta', property='og:image_
