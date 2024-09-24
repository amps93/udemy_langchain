import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()

# 트위터 API 초기화
# .env 파일에서 각 key 받아와야 하나 요금 문제로 사용 X

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets (i.e., nte retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: 'time_posted (relative to now), 'text', and 'url'.
    """
    tweet_list = []
    if mock:  # 정적 파일 사용
        EDEN_TWITTER_GIST = 'https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json'
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()
    else:  # twitter api 사용 - 요금 부과됨
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=['retweets', 'replies']
        )
        tweets = tweets.data

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict['text'] = tweet['text']
        tweet_dict['url'] = f'https://twitter.com/{username}/status/{tweet['id']}'
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == '__main__':
    tweets = scrape_user_tweets(username='EdenEmarco177', mock=True)
    print(tweets)

