from flask import Flask, jsonify
from flask_cors import CORS
from twscrape import API, gather
import asyncio

app = Flask(__name__)
CORS(app)


async def main():
    api = API()  # or API("path-to.db") - default is `accounts.db`

    # ADD ACCOUNTS (for CLI usage see BELOW)
    await api.pool.add_account("myusername", "andmypassword", "email@gmail.com", "pass")
    await api.pool.login_all()

    tweets = await gather(api.user_tweets("1492111965644283910", limit=10))
    tweets_array = []
    for tweet in tweets:
        tweets_array = tweets_array + [{
            'id': tweet.id_str,
            'url': tweet.url,
            'date': str(tweet.date),
            'lang': tweet.lang,
            'rawContent': tweet.rawContent,
            'replyCount': tweet.replyCount,
            'retweetCount': tweet.retweetCount,
            'likeCount': tweet.likeCount,
            'hashtags': tweet.hashtags,
            'viewCount': tweet.viewCount,
            'place': tweet.place
        }]
    return tweets_array


@app.route('/')
def hello_world():
    ls = asyncio.run(main())
    return jsonify(ls)
