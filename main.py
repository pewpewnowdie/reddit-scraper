import requests

def get_request(subreddit, next, time):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time}{next}"

    headers = {
        "User-Agent": "pewpewnowdie"
    }

    response = requests.get(url, headers=headers)
    return response

def get_posts(subreddits, next = '', time = 'week'):
    posts = []
    if type(subreddits) == type([]):
        for subreddit in subreddits:
            response = get_request(subreddit, next, time)
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
                
    elif type(subreddits) == type(''):
        response = get_request(subreddits, next, time)
        response_json = response.json()
        children = response_json['data']['children']
        for i in range (len(children)):
            post = {}
            data = children[i]['data']
            try:
                post['id'] = data['name']
                post['title'] = data['title'] 
                media = data['media']
                post['comments'] = data['num_comments']
                post['upvote_ratio'] = data['upvote_ratio']
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
    else:
        print('argument should be a string')
    return posts

def main():
    subreddits = ['IndianMeyMeys', 'IndianDankMemes']
    posts = get_posts(subreddits)

    for post in posts:
        print(post['title'])