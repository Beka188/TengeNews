from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from News import *
from newsDB import add_news_DB, News, print_db, get_news, if_exist, delete, find_one_news

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def update_db():
    top_news = get_main_page_news(original_link, "")
    sport_news = get_sport_news('https://tengrisport.kz/', "")
    edu_news = get_sport_news('https://tengrinews.kz/tengri-education/', "")
    travel_news = get_travel_news('https://tengritravel.kz/', "")
    trending_news = get_trending_news('https://tengrinews.kz/mixnews/', "")
    popular_news = get_popular_news(original_link, "")
    latest_news = get_latest_news(original_link, "")
    read_more = read_more_news('https://tengrinews.kz/tag/что_будет_с_казахстаном/')
    for news in top_news:
        if not if_exist(news.url, "main"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "main", news.image, news.url)
            add_news_DB(new_news_db)
    for news in edu_news:
        if not if_exist(news.url, "edu"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "edu", news.image, news.url)
            add_news_DB(new_news_db)
    for news in travel_news:
        if not if_exist(news.url, "travel"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "travel", news.image, news.url)
            add_news_DB(new_news_db)
    for news in trending_news:
        if not if_exist(news.url, "trend"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "trend", news.image, news.url)
            add_news_DB(new_news_db)
    for news in popular_news:
        if not if_exist(news.url, "popular"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "popular", news.image, news.url)
            add_news_DB(new_news_db)
    for news in latest_news:
        if not if_exist(news.url, "latest"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "latest", news.image, news.url)
            add_news_DB(new_news_db)
    for news in read_more:
        if not if_exist(news.url, "read_more"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "read_more", news.image, news.url)
            add_news_DB(new_news_db)
    print("SPORT\n")
    for news in sport_news:
        print("TITLEOF\n")
        print(news.title)
        if not if_exist(news.url, "sport"):
            new_news_db = News(news.title, str(get_news_content(news.url)), "sport", news.image, news.url)
            add_news_DB(new_news_db)
    print("DB UPDATED")


scheduler = BackgroundScheduler()
scheduler.start()

# update_db()
# print_db()
# for news in get_news("main"):
#     print(news.title)
#     print(news.date)
#     print()

scheduler.add_job(update_db, trigger=IntervalTrigger(seconds=30))


@app.get("/")
async def main_page(request: Request):
    top_news, sport_news, edu_news, travel_news, trending_news, popular_news, latest_news, read_more = main_page_news_collection()
    return templates.TemplateResponse("index.html", {"request": request, "top_news": top_news, "sport_news": sport_news,
                                                     "edu_news": edu_news, "travel_news": travel_news,
                                                     'trending_news': trending_news, "popular_news": popular_news,
                                                     "latest_news": latest_news, "read_more": read_more})


@app.get("/search/")
async def search(request: Request, text: str = Query(None)):
    searched_news, keyword = get_searched_news(text)
    total_pages = int(len(searched_news) / 10)
    page: int = 0
    return templates.TemplateResponse("search.html", {"request": request, "searched_news": searched_news, "page": page,
                                                      "total_pages": total_pages, "searched_word": text})




@app.get("/news")  # single page
async def open_file(request: Request, title: str = "", image: str = "", url: str = "", category: str = ""):
    # return url
    news = find_one_news(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if news is None:
        article_content = soup.find('div', class_='content_main')
    else:
        article_content = news.content

    related_news = get_related_news(category, title)
    return templates.TemplateResponse("single_page.html", {"request": request, "title": title, "image": image,
                                                           "related_news": related_news,
                                                           "article_content": article_content,
                                                           "url": url})
