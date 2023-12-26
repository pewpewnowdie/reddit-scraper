import requests
import time

class Post:
    def __init__(self, id, title, upvotes, comments, upvote_ratio, subreddit, source, format, dash, video_url, audio_url, image_url):
        self.id = id
        self.title = title
        self.upvotes = upvotes
        self.comments = comments
        self.upvote_ratio = upvote_ratio
        self.subreddit = subreddit
        self.source = source
        self.format = format
        self.dash = dash
        self.video_url = video_url
        self.audio_url = audio_url
        self.image_url = image_url

    def __dir__(self):
        return ['id', 'title', 'upvotes', 'comments', 'upvote_ratio', 'subreddit', 'source', 'format', 'dash', 'video_url', 'audio_url', 'image_url']

def get_request(subreddit, param = '', dura = 'week'):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t={dura}{param}"

    headers = {
        "User-Agent": "pewpewnowdie"
    }

    response = requests.get(url, headers=headers)
    return response

def parse(subreddit, after = '', dura = 'week'):
    posts = []
    time.sleep(1)
    response = get_request(subreddit, after, dura)

    if response.status_code != 200:
        print('Error')
        return posts
    
    response_json = response.json()
    children = response_json['data']['children']

    for i in range (len(children)):
        
        data = children[i]['data']
        try:
            post = Post(data['name'], data['title'], data['ups'], data['num_comments'], data['upvote_ratio'], data['subreddit_name_prefixed'], 'https://www.rxddit.com'+data['permalink'],None, None, None, None, None) 
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
        posts.append(post)
        print(post.id, post.source)

    after = response_json['data']['after']
    if after:
        param = '&after='+response_json['data']['after']
        after_posts = parse(subreddit, param)
        posts = posts + after_posts

    return posts

def get_posts(subreddits, after = '', dura = 'week'):
    posts = []
    try:
        for subreddit in subreddits:
            temp = parse(subreddit, after = after, dura = dura)
            posts = posts + temp
    except KeyboardInterrupt:
        print('Exiting...')
    return posts

def main():
    subreddits = ['IndianDankMemes']
    posts = get_posts(subreddits, after = '', dura = 'day')
    print(len(posts))
    for post in posts:
        print(vars(post))

if __name__ == "__main__":
    main()
