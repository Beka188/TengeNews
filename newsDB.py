from fastapi import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests

Base = declarative_base()


class News(Base):
    __tablename__ = "News"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    content = Column("content", String)
    category = Column("category", String)
    image = Column("image_url", String)
    url = Column("source_url", String)
    date = Column("date", DateTime, default=func.now())

    def __init__(self, title, content, category, image, url):
        self.title = title
        self.content = content
        self.category = category
        self.image = image
        self.url = url

    def __repr__(self):
        return f"{self.title} {self.content} {self.category} {self.image} {self.url}"


engine = create_engine("sqlite:///NEWS.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_news_DB(news: News):
    session.add(news)
    if is_news_valid(news):
        session.commit()
        return True
    return False


def is_news_valid(news: News):
    if is_valid_url(news.image) and is_valid_url(news.url):
        return True
    return False


def is_valid_url(url):
    try:
        response = requests.head(url)
        return True
    except requests.RequestException:
        return False


# Print each row
def print_db():
    news = session.query(News).all()
    for user in news:
        print(user.category)
        print(user.title)
        print(user.date)
        print()


def get_news(category: str):
    news_results = session.query(News).filter(News.category.like(f"%{category}%")).order_by(desc(News.date)).all()
    return news_results


def if_exist(url: str, category: str):
    if session.query(News).filter_by(url=str(url), category=category).first() is not None:
        return True
    else:
        return False

def find_one_news(url: str):
    try:
        return session.query(News).filter_by(url=str(url)).first()
    except:
        return None

def delete():
    session.query(News).delete()
    session.commit()
