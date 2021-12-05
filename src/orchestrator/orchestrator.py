"""
Orchestrator/Driver for the application.
"""
import datetime as dt
from sqlite3.dbapi2 import connect

from twitter_utils.tweet_reader import TweetReader
from twitter_utils.tweet_sentiment import TwitterSentimentAnalyzer
from database_utils.sqlite_writer import SqliteWriter


def main():
    """
    Main entry point for the script.
    """

    # Setup paths
    config_path = ".\\src\\uncommitted\\config.ini"
    credentials_path = ".\\src\\uncommitted\\credentials.ini"

    # Setup twitter API
    tweet_reader: TweetReader = TweetReader(
        config_path=config_path, api_credentials_path=credentials_path
    )

    # Collect twitter data in dataframe
    tweets_df = tweet_reader.get_all_tweets()

    # Parse tweets
    sentiment_analyzer = TwitterSentimentAnalyzer()
    tweets_df["tweet"] = sentiment_analyzer.disable_hyperlinks_from_tweets(
        tweets_df["tweet"]
    )

    # Analyze sentiment of twitter data
    analyzed_tweets_df = sentiment_analyzer.add_sentiment_score_to_tweet(
        tweets_df=tweets_df, tweet_col_name="tweet"
    )

    # Setup writer for sql database
    sql_db_writer = SqliteWriter(config_path=config_path)

    # Append dataframe to the Sqlite database
    sql_db_writer.append_dataframe_to_sql_table(analyzed_tweets_df)


if __name__ == "__main__":
    main()
