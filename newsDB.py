from sqlalchemy import create_engine, Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from News import News as News_Class
Base = declarative_base()

class News(Base):
    __tablename__ = "News"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    content = Column("content", String)
    published_date = Column("published_date", Date)
    category = Column("category", String)
    image_url = Column("image_url", String)
    source_url = Column("source_url", String)


    def __init__(self, title, content, published_date, category, image_url, source_url):
        self.title = title
        self.content = content
        self.published_date = published_date
        self.category = category
        self.image_url = image_url
        self.source_url = source_url

    def __repr__(self):
        return f"{self.title} {self.content} {self.published_date} {self.category} {self.image_url} {self.source_url} {self.description}"


engine = create_engine("sqlite:///Advertisements.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_news(news: News_Class):
    new_news = News(news.title, news.url, news.image)



# def add_advertisement(user, data: Addd):
#     ad = Advertisement(user, data.type, data.price, data.address, data.area, data.rooms_count, data.description)
#     session.add(ad)
#     session.commit()
#     return ad.id
