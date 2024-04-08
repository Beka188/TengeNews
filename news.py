from sqlalchemy import create_engine, Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

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
    views = Column("views", Integer)
    likes = Column("likes", Integer)
    comments = Column("comments", Integer)
    keywords = Column("keywords", )

    def __init__(self, user, tip, price, address, area, rooms_count, description):
        self.user = user
        self.type = tip
        self.price = price
        self.address = address
        self.area = area
        self.rooms_count = rooms_count
        self.description = description

    def __repr__(self):
        return f"{self.id} {self.user} {self.type} {self.address} {self.area} {self.rooms_count} {self.description}"


engine = create_engine("sqlite:///Advertisements.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

