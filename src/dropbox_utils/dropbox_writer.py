"""
Module to write the processed data to dropbox.
"""
from configparser import ConfigParser
from typing import Optional
from dropbox import Dropbox


class DropboxWriter:
    """
    A class to setup and leverage the dropbox API.
    """
    def __init__(self, config_path: str, api_credentials_path: str) -> None:

        self.config = ConfigParser()
        self.config.read(config_path)

        self.credentials: ConfigParser = ConfigParser()
        self.credentials.read(api_credentials_path)

        self.api = None
        self.__config_api()

    def __config_api(self) -> Dropbox:
        """
        Configure the dropbox API.
        """

        token: str = self.credentials.get("DROPBOX", "token")

        self.api = Dropbox(token)

    def write_raw_file_to_dropbox(
        self, data: str, file_name: str, encoding: Optional[str] = "utf-8"
    ):
        """
        Basic writer function for the class.
        """
        write_path = (
            f"""{self.config.get("OUTPUT", "dropbox_write_path")}/{file_name}"""
        )
        self.api.files_upload(data.encode(encoding), path=write_path)
