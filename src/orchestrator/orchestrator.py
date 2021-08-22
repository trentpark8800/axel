"""
Orchestrator/Driver for the application.
"""
import datetime as dt

from twitter_utils.tweet_reader import TweetReader
from twitter_utils.tweet_sentiment import TwitterSentimentAnalyzer
from dropbox_utils.dropbox_writer import DropboxWriter


def main():

    # Setup paths
    config_path = "./src/uncommitted/config.ini"
    credentials_path = "./src/uncommitted/credentials.ini"

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

    # Instantiate dropbox writer
    dropbox_writer = DropboxWriter(
        config_path=config_path, api_credentials_path=credentials_path
    )

    # Convert dataframe to string for dropbox upload
    data_string: str = tweets_df.to_csv()

    # Upload to dropbox
    file_name = (
        f"daily_tweets_{dt.datetime.strftime(dt.date.today(), format='%Y%m%d')}.csv"
    )
    dropbox_writer.write_raw_file_to_dropbox(data=data_string, file_name=file_name)


if __name__ == "__main__":
    main()
