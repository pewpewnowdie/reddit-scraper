import requests
import time



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
        post = {}
        data = children[i]['data']
        try:
            post['id'] = data['name']
            post['title'] = data['title'] 
            media = data['media']
            post['upvotes'] = data['ups']
            post['comments'] = data['num_comments']
            post['upvote_ratio'] = data['upvote_ratio']
            post['subreddit'] = data['subreddit_name_prefixed']
            post['source'] = 'https://www.rxddit.com'+data['permalink']
            if(media):
                post['dash'] = media['reddit_video']['dash_url']
                post['video_url'] = media['reddit_video']['fallback_url']
                post['audio_url'] = post['video_url'][0:post['video_url'].rfind('DASH_') + 5] + 'AUDIO_64.mp4'
                post['image_url'] = None
            else:
                if data['url_overridden_by_dest'][0:17] != 'https://i.redd.it':
                    continue
                post['format'] = 'image'
                post['dash'] = None
                post['video_url'] = None
                post['audio_url'] = None
                post['image_url'] = data['url_overridden_by_dest']
        except:
            continue
        posts.append(post)
        print(post['id'], post['source'])

    after = response_json['data']['after']
    if after:
        param = '&after='+response_json['data']['after']
        after_posts = parse(subreddit, param)
        posts = posts + after_posts

    return posts



def get_posts(subreddits, dura = 'day'):
    posts = []
    try:
        for subreddit in subreddits:
            temp = parse(subreddit, dura = dura)
            posts = posts + temp
    except KeyboardInterrupt:
        print('Exiting...')
    return posts



def main():
    subreddits = ['IndianDankMemes']
    posts = get_posts(subreddits)
    print(len(posts))
    for post in posts:
        if post['format'] == 'video':
            print(post['video_url'])



if __name__ == "__main__":
    main()
