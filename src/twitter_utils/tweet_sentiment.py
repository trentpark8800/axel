"""
Module for scoring tweet sentiments in dataframe columns.
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pandas import read_csv
from pandas.core.frame import DataFrame, Series


class TwitterSentimentAnalyzer:
    def __init__(self) -> None:

        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    @staticmethod
    def disable_hyperlinks_from_tweets(tweet_series: Series) -> Series:
        return tweet_series.replace("://", "//")

    def add_sentiment_score_to_tweet(
        self, tweets_df: DataFrame, tweet_col_name: str
    ) -> DataFrame:

        # Extract normalized score (sentiment value is between -1 and +1)
        tweets_df["compound_sentiment_score"] = tweets_df[tweet_col_name].apply(
            lambda tweet: self.sentiment_analyzer.polarity_scores(tweet)["compound"]
        )

        return tweets_df
