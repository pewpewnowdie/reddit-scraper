from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func

db = 'sqlite:///lib/posts.db'
engine = create_engine(db, echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    post_id = Column(String, unique=True)
    title = Column(String)
    upvotes = Column(Integer)
    comments = Column(Integer)
    upvote_ratio = Column(Float)
    subreddit = Column(String)
    source = Column(String)
    format = Column(String)
    dash = Column(String)
    video_url = Column(String)
    audio_url = Column(String)
    image_url = Column(String)

# Base.metadata.create_all(engine)

def get_random(base):
    return session.query(base).order_by(func.random()).limit(1).first()

print(get_random(Post).post_id)