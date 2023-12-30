import requests
import time
from db import Post, session

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
        param = '&after=' + after
        parse(subreddit, param)


def get_posts(subreddits, after = '', dura = 'week'):
    try:
        for subreddit in subreddits:
            parse(subreddit, after = after, dura = dura)
    except KeyboardInterrupt:
        print('Exiting...')


def main():
    subreddits = ['sunraybee']
    get_posts(subreddits, after = '', dura = 'day')


if __name__ == "__main__":
    main()
