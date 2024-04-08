from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from News import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main_page(request: Request):
    top_news, sport_news, edu_news, travel_news, trending_news, popular_news, latest_news, read_more = main_page_news_collection()
    return templates.TemplateResponse("index.html", {"request": request, "top_news": top_news, "sport_news": sport_news,
                                                     "edu_news": edu_news, "travel_news": travel_news,
                                                     'trending_news': trending_news, "popular_news": popular_news,
                                                     "latest_news": latest_news, "read_more": read_more})


@app.get("/search/")
async def search(request: Request, text: str = Query(None)):
    searched_news = get_searched_news(text)
    return templates.TemplateResponse("search.html", {"request": request, "searched_news": searched_news})


@app.get("/news")  # single page
async def open_file(request: Request, title: str, image: str, category: str = ""):
    url = 'https://tengrinews.kz/kazakhstan_news/zdanie-universiteta-zaminirovali-pod-almatyi-531626/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_content = soup.find('div', class_='content_main')
    related_news = get_related_news(category, title)
    return templates.TemplateResponse("single_page.html", {"request": request, "title": title, "image": image,
                                                           "related_news": related_news,
                                                           "article_content": article_content})

get_popular_news(original_link, "")
