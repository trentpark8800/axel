"""
Module to add sentiment scores to raw tweets.
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from pandas.core.frame import DataFrame, Series


def disable_hyperlinks_from_tweets(tweet_series: Series) -> Series:
    return tweet_series.replace("://", "//")


def add_sentiment_score_to_tweet(tweets_df: DataFrame, sentiment_analyzer: SentimentIntensityAnalyzer) -> DataFrame:

    # Calculate scores, i.e. positive, neutral or negative
    tweets_df['sentiment_scores'] = tweets_df['tweet'].apply(lambda tweet: sentiment_analyzer.polarity_scores(tweet))

    # Extract normalized score (sentiment value is between -1 and +1)
    tweets_df['compound_sentiment'] = tweets_df['sentiment_scores'].apply(lambda scores: scores['compound'])

    return tweets_df


def main():
    # Read in data
    tweets_df = pd.read_csv("./data/raw/standard_bank_tweets.csv")

    # Clean tweet text - remove all hyperlinks to prevent accidental clicks
    tweets_df["tweet"] = disable_hyperlinks_from_tweets(tweets_df["tweet"])

    # Instantiate sentiment analyzer - uses vader lexicon by default
    sia = SentimentIntensityAnalyzer()

    # Add sentiment to dataframe
    tweets_df = add_sentiment_score_to_tweet(tweets_df, sia)

    # Write to staging location
    tweets_df.to_csv("./data/stage/staged_tweets.csv", index=False)


if __name__ == "__main__":
    main()
