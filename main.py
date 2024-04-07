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


# print(news[original_link + news.a.picture.source['srcset']])
class News:
    image: str
    title: str
    url: str

    def __init__(self, image, title, url):
        self.image = image
        self.title = title
        self.url = url


def get_main_page_news(link: str):
    page_news = []
    html_text = requests.get(link + '/news').text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='content_main_item')
    for new in news:
        url = original_link + new.a['href']
        image_link = original_link + new.find('img', class_='content_main_item_img')['src']
        title = new.find('span', class_='content_main_item_title').text
        new_news = News(image_link, title, url)
        page_news.append(new_news)
        if len(page_news) == 5:
            break

    return page_news

def get_sport_news(link: str):
    page_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='main-news_super_item')
    print(news)
    for new in news:
        url = original_link + new.a['href']
        image_link = original_link + new.find('img', class_='main-news_super_item_img')['src']
        title = new.find('span', class_='main-news_super_item_title').text
        new_news = News(image_link, title, url)
        page_news.append(new_news)
        print(url)
        print(image_link)
        print(title)
        print()
        print()
    return page_news

# print(get_sport_news('https://tengrisport.kz/'))
@app.get("/")
async def main_page(request: Request):
    top_news = get_main_page_news(original_link)
    sport_news = get_sport_news('https://tengrisport.kz/')
    edu_news = get_sport_news('https://tengrinews.kz/tengri-education/')
    return templates.TemplateResponse("index.html", {"request": request, "top_news": top_news, "sport_news": sport_news, "edu_news": edu_news})
