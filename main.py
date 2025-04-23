from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import datetime

app = FastAPI()

class LinkRequest(BaseModel):
    url: str

@app.post("/crawl")
async def crawl_news(data: LinkRequest):
    url = data.url
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    response.encoding = 'euc-kr'  # 기존 코드와 동일하게 인코딩 처리

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출
    title_tag = soup.select_one('h1.subject')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title'

    # 본문 추출
    content_div = soup.select_one('div.view_text')
    content = content_div.get_text(strip=True).replace('\xa0', ' ') if content_div else 'No Content'

    # 이미지 추출
    img_tag = soup.select_one('div.view_img img') or soup.select_one('div.view_text img')
    image_url = img_tag['src'] if img_tag else 'No Image'

    # 날짜 포함해서 응답
    today_date = datetime.date.today().isoformat()

    return {
        'title': title,
        'content': content,
        'image_url': image_url,
        'date': today_date,
        'shorts_done': 'No',
        'upload_done': 'No'
    }
