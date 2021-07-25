from configparser import ConfigParser
from typing import List
from tweepy import OAuthHandler, API, Cursor
import pandas as pd
from pandas import DataFrame
import datetime as dt
import time


def config_api(config_path: str) -> API:

    config: ConfigParser = ConfigParser()
    config.read(config_path)

    consumer_key = config.get("TwitterAPI", "api_key")
    consumer_secret = config.get("TwitterAPI", "api_secret_key")
    access_token = config.get("TwitterAPI", "access_token")
    access_token_secret = config.get("TwitterAPI", "access_token_secret")

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth, wait_on_rate_limit=True)

    return api


def get_tweets(query: str, api: API, geocode: str, count_limit: int) -> DataFrame:
    try:
        # Creation of query method using parameters
        tweets = Cursor(api.search, q=query, geocode=geocode, tweet_mode='extended').items(count_limit)

        # Pulling information from tweets iterable object
        tweets_list = [
            [query, tweet.created_at, tweet.id, tweet.full_text, tweet.retweet_count]
            for tweet in tweets
        ]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        column_names: List = ["query", "created_at", "tweet_id", "tweet", "retweets"]
        tweets_df = pd.DataFrame(tweets_list, columns=column_names)

        return tweets_df

    except BaseException as e:
        print("failed on_status,", str(e))
        time.sleep(3)


def parse_tweets(tweets_df: DataFrame, string_patterns: List[str]) -> DataFrame:

    return tweets_df


def main():
    api: API = config_api("./credentials.ini")

    # Create a specific query for twitter cursor
    query = "$JSESBK exclude:retweets exclude:replies"#"('$SBK' OR '$JSE:SBK') exclude:retweets exclude:replies"
    # Specify longitude, latitude and radius to search
    geocode = "-28.8166236,24.991639,1000km"
    sbg_tweets_df = get_tweets(query, api, geocode, 150)

    # Write the tweets to a csv file
    write_base_path = "./data/raw/"
    sbg_tweets_df.to_csv(f"../{write_base_path}/standard_bank_tweets.csv", index=False)


if __name__ == "__main__":
    main()
