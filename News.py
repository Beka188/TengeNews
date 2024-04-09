import requests
from bs4 import BeautifulSoup


class News:
    image: str
    title: str
    url: str

    def __init__(self, image, title, url):
        self.image = image
        self.title = title
        self.url = url


original_link = 'https://tengrinews.kz'
image_not_found = "https://www.google.com/imgres?q=image%20not%20found&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F1409329028%2Fvector%2Fno-picture-available-placeholder-thumbnail-icon-illustration-design.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3D_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ%3D&imgrefurl=https%3A%2F%2Fwww.istockphoto.com%2Fvector%2Fno-picture-available-placeholder-thumbnail-icon-illustration-design-gm1409329028-459910308&docid=vMH7vQlbUCQfAM&tbnid=Oo2FlwD8DLKyVM&vet=12ahUKEwimvenflrOFAxUEIxAIHaulCHYQM3oECBkQAA..i&w=612&h=437&hcb=2&ved=2ahUKEwimvenflrOFAxUEIxAIHaulCHYQM3oECBkQAA"


def get_main_page_news(link: str, remove: str):
    page_news = []
    html_text = requests.get(link + '/news').text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='content_main_item')
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        try:
            image_link = original_link + new.find('img', class_='content_main_item_img')['src']
        except (AttributeError, TypeError):
            image_link = image_not_found
        title = new.find('span', class_='content_main_item_title').text
        if title.strip().lower() != remove.strip().lower():
            new_news = News(image_link, title, url)
            page_news.append(new_news)

        if len(page_news) == 6:
            break
    return page_news


def get_sport_news(link: str, remove: str):
    page_news: [News] = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='main-news_super_item')
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        try:
            image_link = original_link + new.find('img', class_='main-news_super_item_img')['src']
        except (AttributeError, TypeError):
            image_link = image_not_found
        title = str(new.find('span', class_='main-news_super_item_title').text)
        if title.strip().lower() != remove.strip().lower():
            new_news = News(image_link, title, url)
            page_news.append(new_news)

    return page_news


def get_travel_news(link: str, remove: str):
    travel_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('article',
                         class_='grid-item post type-post status-publish format-standard has-post-thumbnail hentry category-around-the-world')
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        try:
            image_link = original_link + new.find('img', class_='attachment- size- wp-post-image')['src']
        except (AttributeError, TypeError):
            image_link = image_not_found
        title = new.find('h2', class_='entry-title').text
        if title.strip().lower() != remove.strip().lower():
            new_news = News(image_link, title, url)
            travel_news.append(new_news)

    return travel_news


def get_trending_news(link: str, remove: str):
    trending_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div',
                         class_='blog-post miami')
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        figure_tag = new.find('figure', class_='post-image')
        try:
            image_link = original_link + figure_tag.find('img')['src']
        except (AttributeError, TypeError):
            image_link = image_not_found
        title = new.find('h3', class_='post-title').text
        if title.strip().lower() != remove.strip().lower():
            new_news = News(image_link, title, url)
            trending_news.append(new_news)

    return trending_news


def get_searched_news(searched_word: str):
    searched_news = []
    html_text = requests.get(f'https://tengrinews.kz/search/?text={searched_word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_='content_main_item')
    i = 0
    for new in news:
        if i == 10:
            break
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        try:
            image_link = new.find('img', class_='content_main_item_img')['src']
        except TypeError:
            image_link = image_not_found
        title = new.find('span', class_='content_main_item_title').text
        new_news = News(image_link, title, url)
        searched_news.append(new_news)

        i += 1
    return searched_news


def get_related_news(category: str, remove_news_title: str):
    if category == "sport":
        return get_sport_news("https://tengrisport.kz/", remove_news_title)
    elif category == "education":
        return get_sport_news('https://tengrinews.kz/tengri-education/', remove_news_title)
    elif category == "travel":
        return get_travel_news('https://tengritravel.kz/', remove_news_title)
    elif category == "trend":
        return get_trending_news('https://tengrinews.kz/mixnews/', remove_news_title)
    elif category == "recent":
        return get_popular_news(original_link, remove_news_title)
    else:
        return get_main_page_news(original_link, remove_news_title)


def get_popular_news(link: str, remove: str):
    popular_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news_top = soup.find('div',
                         id='content-2')
    news = news_top.find_all('div', class_="main-news_top_item")
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        image_html = requests.get(url).text
        soup = BeautifulSoup(image_html, "lxml")
        figure = soup.find('div', class_="content_main_thumb")
        try:
            image_link = original_link + figure.find('img')['src']
            title = new.find('span', class_='main-news_top_item_title').text
            if title.strip().lower() != remove.strip().lower():
                new_news = News(image_link, title, url)
                popular_news.append(new_news)
        except (AttributeError, TypeError) as e:
            print(f"Error: {e}")
            continue
        # print(url)
        if remove == "" and len(popular_news) == 4:
            break
        elif remove != "" and len(popular_news) == 7:
            break

    return popular_news


def get_latest_news(link: str, remove: str):
    latest_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news_top = soup.find('div',
                         id='content-1')
    news = news_top.find_all('div', class_="main-news_top_item")
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        image_html = requests.get(url).text
        soup = BeautifulSoup(image_html, "lxml")
        figure = soup.find('div', class_="content_main_thumb")
        try:
            image_link = original_link + figure.find('img')['src']
        except (AttributeError, TypeError):
            image_link = "https://www.google.com/imgres?q=image%20not%20found&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F1409329028%2Fvector%2Fno-picture-available-placeholder-thumbnail-icon-illustration-design.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3D_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ%3D&imgrefurl=https%3A%2F%2Fwww.istockphoto.com%2Fvector%2Fno-picture-available-placeholder-thumbnail-icon-illustration-design-gm1409329028-459910308&docid=vMH7vQlbUCQfAM&tbnid=Oo2FlwD8DLKyVM&vet=12ahUKEwimvenflrOFAxUEIxAIHaulCHYQM3oECBkQAA..i&w=612&h=437&hcb=2&ved=2ahUKEwimvenflrOFAxUEIxAIHaulCHYQM3oECBkQAA"  # or any other default value you want
        title = new.find('span', class_='main-news_top_item_title').text
        if title.strip().lower() != remove.strip().lower():
            new_news = News(image_link, title, url)
            latest_news.append(new_news)
        if remove == "" and len(latest_news) == 7:
            break
        elif remove != "" and len(latest_news) == 7:
            break

    return latest_news


def read_more_news(link: str):
    more_news = []
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('div', class_="content_main_item")
    for new in news:
        url = new.a['href']
        if url[:5] != "https":
            url = original_link + url
        try:
            image_link = original_link + new.find('img')['src']
        except (AttributeError, TypeError):
            image_link = image_not_found  # or any other default value you want
        title = new.find('span', class_="content_main_item_title").text
        new_news = News(image_link, title, url)
        more_news.append(new_news)
        if len(more_news) == 6:
            break
    return more_news


def main_page_news_collection():
    top_news = get_main_page_news(original_link, "")
    sport_news = get_sport_news('https://tengrisport.kz/', "")
    edu_news = get_sport_news('https://tengrinews.kz/tengri-education/', "")
    travel_news = get_travel_news('https://tengritravel.kz/', "")
    trending_news = get_trending_news('https://tengrinews.kz/mixnews/', "")
    popular_news = get_popular_news(original_link, "")
    latest_news = get_latest_news(original_link, "")
    read_more = read_more_news('https://tengrinews.kz/tag/что_будет_с_казахстаном/')
    return top_news, sport_news, edu_news, travel_news, trending_news, popular_news, latest_news, read_more
