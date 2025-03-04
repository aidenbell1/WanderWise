import tweepy

# Twitter API credentials
api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"
access_secret = "your_access_secret"

# Authenticate
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Fetch tweets about Paris travel
tweets = api.search_tweets(q="Paris travel", lang="en", count=10)
for tweet in tweets:
    print(tweet.text)