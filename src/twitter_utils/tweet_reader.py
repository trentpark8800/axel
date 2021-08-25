"""
Module for reading tweets using the twitter API via the tweepy package.
"""
from configparser import ConfigParser
from typing import Dict, List
from tweepy import OAuthHandler, API, Cursor
import pandas as pd
from numpy import isnan
from pandas import DataFrame
import time
from json import load as load_json


class TweetReader:
    """
    A class to leverage the twitter API to read tweets.
    """

    def __init__(self, config_path: str, api_credentials_path: str) -> None:

        self.config: ConfigParser = ConfigParser()
        self.config_path = config_path
        self.config.read(self.config_path)

        self.api_credentials_path = api_credentials_path
        self.credentials: ConfigParser = ConfigParser()
        self.credentials.read(self.api_credentials_path)
        self.api = None
        self.__config_api()

    def __config_api(self) -> None:
        """
        Configure the Tweepy API object.
        """

        consumer_key = self.credentials.get("TwitterAPI", "api_key")
        consumer_secret = self.credentials.get("TwitterAPI", "api_secret_key")
        access_token = self.credentials.get("TwitterAPI", "access_token")
        access_token_secret = self.credentials.get("TwitterAPI", "access_token_secret")

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth, wait_on_rate_limit=True)

    def get_batch_of_tweets(
        self, company_name, query: str, geocode: str, last_tweet_id: int
    ) -> DataFrame:
        """
        Get a single 'batch' of tweets according to a single twitter query.
        """
        try:
            # Creation of query method using parameters
            tweets = Cursor(
                self.api.search,
                q=query,
                geocode=geocode,
                since_id=last_tweet_id,
                tweet_mode="extended",
            ).items()

            # Pulling information from tweets iterable object
            tweets_list = [
                [
                    company_name,
                    query,
                    tweet.created_at,
                    tweet.id,
                    tweet.full_text,
                    tweet.retweet_count,
                ]
                for tweet in tweets
            ]

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            # TODO: Specify datatypes for efficiency
            column_names: List = [
                "company_or_index",
                "query",
                "created_at",
                "tweet_id",
                "tweet",
                "retweets",
            ]
            tweets_df = pd.DataFrame(tweets_list, columns=column_names)

            return tweets_df

        except BaseException as e:
            print("failed on_status,", str(e))
            time.sleep(3)

    def get_all_tweets(self):
        """
        Iterator that uses the query dict to fetch tweets associated
        with different queries.
        """

        query_dict_path: str = self.config.get("QUERIES", "query_dict_path")
        last_tweet_id: int = int(self.config.get("TWEETS", "last_tweet_id"))

        # Create empty tweets df for concat in query loop
        column_names: List = [
            "company_or_index",
            "query",
            "created_at",
            "tweet_id",
            "tweet",
            "retweets",
        ]
        tweets_df: DataFrame = pd.DataFrame(columns=column_names)

        with open(query_dict_path) as f:
            query_dict: Dict = load_json(f)
            f.close()

        # TODO: Add a query dict parser to check for expected elements

        for company in query_dict.keys():
            query_text: str = query_dict[company]["query"]
            geocode: str = query_dict[company]["geocode"]

            _temp_df: DataFrame = self.get_batch_of_tweets(
                company_name=company,
                query=query_text,
                geocode=geocode,
                last_tweet_id=last_tweet_id,
            )

            tweets_df = pd.concat([tweets_df, _temp_df])

        # Update last tweet id for next batches of tweets
        # If the df is empty, i.e. no tweets then don't modify last
        # tweet id in config
        max_tweet_id = tweets_df["tweet_id"].max()
        if isnan(max_tweet_id):
            return tweets_df

        self.config["TWEETS"]["last_tweet_id"] = str(max_tweet_id)
        with open(self.config_path, "w") as f:
            self.config.write(f)
            f.close()

        return tweets_df
