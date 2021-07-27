"""
Module to write the processed data to dropbox.
"""
import datetime as dt
from configparser import ConfigParser
from typing import Optional
from dropbox import Dropbox


def config_dropbox_api(config_path: str) -> Dropbox:

    config: ConfigParser = ConfigParser()
    config.read(config_path)

    token: str = config.get("DROPBOX", "token")

    dbx = Dropbox(token)

    return dbx


def read_file_into_string(file_path: str) -> str:

    with open(file_path) as f:
        data: str = f.read()
        f.close()
    return data


def write_raw_file_to_dropbox(
    dbx: Dropbox, data: str, write_path: str, encoding: Optional[str] = "utf-8"
):

    dbx.files_upload(data.encode(encoding), path=write_path)


def main():
    # Read in staged data
    staged_data = read_file_into_string("./data/stage/staged_tweets.csv")

    # Connect to dropbox via the api
    dbx: Dropbox = config_dropbox_api("./data_load/credentials.ini")

    # Write data to dropbox
    date_today: dt.date = dt.date.today()
    write_path = f"/dev/daily_tweets_{dt.datetime.strftime(date_today, '%Y%m%d')}.csv"
    write_raw_file_to_dropbox(dbx=dbx, data=staged_data, write_path=write_path)


if __name__ == "__main__":
    main()
