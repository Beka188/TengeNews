from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import jinja2
import uvicorn
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

original_link = 'https://tengrinews.kz'
html_text = requests.get(original_link + '/news').text
soup = BeautifulSoup(html_text, 'lxml')
news = soup.find_all('div', class_='content_main_item')

# print(news[original_link + news.a.picture.source['srcset']])
class News:
    image: str
    title: str
    url: str

    def __init__(self, image, title, url):
        self.image = image
        self.title = title
        self.url = url


top_news = []
i = 0
for new in news:
    url = original_link + new.a['href']
    image_link = original_link + new.find('img', class_='content_main_item_img')['src']
    title = new.find('span', class_='content_main_item_title').text

    new_news = News(image_link, title, url)
    top_news.append(new_news)

#
# top_news = [
#     {
#         'image': 'img/news-450x350-1.jpg',
#         'title': 'DFJFDJJSDF',
#         'url': 'http://example.com/news1'
#     },
#     {
#         'image': 'img/news-450x350-2.jpg',
#         'title': 'Integer hendrerit elit eget purus sodales maximus',
#         'url': 'http://example.com/news2'
#     },
#     # Add more news articles as needed
# ]

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "top_news": top_news, "enumerate": enumerate})
