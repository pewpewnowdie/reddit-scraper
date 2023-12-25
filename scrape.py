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
            else:
                post['dash'] = media
        except:
            break
        posts.append(post)
        print(post['id'], min(post['title'][0:25],post['title'][0:len(post['title'])]), '...')

    after = response_json['data']['after']
    if after:
        param = '&after='+response_json['data']['after']
        after_posts = parse(subreddit, param)
        posts = posts + after_posts

    return posts



def get_posts(subreddits, dura = 'week'):
    posts = []
    for subreddit in subreddits:
        temp = parse(subreddit, dura = dura)
        posts = posts + temp
    return posts



def main():
    subreddits = ['India']
    posts = get_posts(subreddits)
    print(len(posts))



if __name__ == "__main__":
    main()
