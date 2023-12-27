import requests
import time
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

db = 'sqlite:///posts.db'
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


def get_request(subreddit, param = '', dura = 'week'):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t={dura}{param}"

    headers = {
        "User-Agent": "pewpewnowdie"
    }

    response = requests.get(url, headers=headers)
    return response


def parse(subreddit, after = '', dura = 'week'):
    time.sleep(1)
    response = get_request(subreddit, after, dura)

    if response.status_code != 200:
        print('Error')
        return
    
    response_json = response.json()
    children = response_json['data']['children']

    for i in range (len(children)):
        data = children[i]['data']
        try:
            post = Post(
                post_id = data['name'], title = data['title'], upvotes = data['ups'], comments = data['num_comments'], upvote_ratio = data['upvote_ratio'], subreddit = data['subreddit_name_prefixed'], source = 'https://www.rxddit.com'+data['permalink'], format = None, dash = None, video_url = None, audio_url = None, image_url = None
                ) 
            media = data['media']
            if media:
                post.format = 'video'
                post.dash = media['reddit_video']['dash_url']
                post.video_url = media['reddit_video']['fallback_url']
                post.audio_url = post.video_url[0:post.video_url.rfind('DASH_') + 5] + 'AUDIO_64.mp4'
            else:
                if data['url_overridden_by_dest'][0:17] != 'https://i.redd.it':
                    continue
                post.format = 'image'
                post.image_url = data['url_overridden_by_dest']
        except:
            continue
        
        existing_entry = session.query(Post).filter_by(post_id = post.post_id).first()

        if existing_entry is None:
            session.add(post)
            session.commit()
        print(post.post_id, post.source)

    after = response_json['data']['after']
    if after:
        param = '&after='+response_json['data']['after']
        parse(subreddit, param)


def get_posts(subreddits, after = '', dura = 'week'):
    try:
        for subreddit in subreddits:
            parse(subreddit, after = after, dura = dura)
    except KeyboardInterrupt:
        print('Exiting...')


def main():
    subreddits = ['IndianDankMemes']
    get_posts(subreddits, after = '', dura = 'week')


if __name__ == "__main__":
    main()
