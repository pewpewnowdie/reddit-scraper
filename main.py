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
            else:
                post['dash'] = media
        except:
            break
        posts.append(post)
    after = response_json['data']['after']
    if after:
        param = '&after='+response_json['data']['after']
        after_posts = parse(subreddit, param)
        posts = posts + after_posts
    return posts

def get_posts(subreddits, after = '', dura = 'week'):
    posts = []
    for subreddit in subreddits:
        temp = parse(subreddit, after, dura)
        time.sleep(1)
        posts = posts + temp
    return posts

def main():
    subreddits = ['programming', 'India']
    posts = get_posts(subreddits)
    print(len(posts))

main()