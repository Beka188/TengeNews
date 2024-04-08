from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import jinja2
import uvicorn
import time

from requests_html2 import HTMLResponse

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


def get_views_comments(link: str):
    html = requests.get(link + '/news')
    time.sleep(10)
    html_text = html.text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', 'content_main_item')
    for new in news:
        views = new.find('span', class_='tn-text-preloader-dark')
        print(views)


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


def get_travel_news(link: str):
    travel_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('article',
                         class_='grid-item post type-post status-publish format-standard has-post-thumbnail hentry category-around-the-world')
    for new in news:
        url = original_link + new.a['href']
        image_link = original_link + new.find('img', class_='attachment- size- wp-post-image')['src']
        title = new.find('h2', class_='entry-title').text
        new_news = News(image_link, title, url)
        travel_news.append(new_news)
    return travel_news


def get_trending_news(link: str):
    trending_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div',
                         class_='blog-post miami')
    for new in news:
        url = original_link + new.a['href']
        figure_tag = new.find('figure', class_='post-image')
        image_link = original_link + figure_tag.find('img')['src']
        title = new.find('h3', class_='post-title').text
        new_news = News(image_link, title, url)
        # print(new_news.title)
        # print(new_news.image)
        # print(new_news.url)
        # print()
        # print()
        trending_news.append(new_news)

    return trending_news


# print(get_sport_news('https://tengrisport.kz/'))


# get_views_comments(original_link)
# from requests_html2 import HTMLSession
# session = HTMLSession()
#
# r = session.get(original_link)
# r.html.render(sleep = 1, scrolldown = 5)
# print(r)
get_trending_news('https://tengrinews.kz/mixnews/')


@app.get("/")
async def main_page(request: Request):
    top_news = get_main_page_news(original_link)
    sport_news = get_sport_news('https://tengrisport.kz/')
    edu_news = get_sport_news('https://tengrinews.kz/tengri-education/')
    travel_news = get_travel_news('https://tengritravel.kz/')
    trending_news = get_trending_news('https://tengrinews.kz/mixnews/')
    return templates.TemplateResponse("index.html", {"request": request, "top_news": top_news, "sport_news": sport_news,
                                                     "edu_news": edu_news, "travel_news": travel_news,
                                                     'trending_news': trending_news})



@app.get("/news")
async def open_file(request: Request, title: str, image: str):
    return templates.TemplateResponse("single_page.html", {"request": request, "title": title, "image": image})



def get_searched_news(searched_word: str):
    searched_news = []
    html_text = requests.get(f'https://tengrinews.kz/search/?text={searched_word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='content_main_item')
    for new in news:
        url = original_link + new.a['href']
        image_link = original_link + new.find('img', class_='content_main_item_img')['src']
        title = new.find('span', class_='content_main_item_title').text
        new_news = News(image_link, title, url)
        print(new_news.title)
        print(new_news.image)
        print(new_news.url)
        print()
        print()
        searched_news.append(new_news)
    return searched_news

@app.get("/search/")
async def search(text: str = Query(None)):
    # Perform your search logic here using the text parameter
    if text:
        return {"text": text}
    else:
        return {"message": "No search query provided"}


# image_url, title, content, category