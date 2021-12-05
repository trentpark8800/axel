"""
Module to create an sqlite db if it does not exist, and write data to the db.
"""
from configparser import ConfigParser
import sqlite3
from sqlite3 import Error

import pandas as pd
from pandas import DataFrame

class SqliteWriter:

    def __init__(self, config_path: str) -> None:

        self.config: ConfigParser = ConfigParser()
        self.config_path = config_path
        self.config.read(self.config_path)

        self.db_file = self.config.get("SQLITE", "database_name")
        self.table_name = self.config.get("SQLITE", "table_name")
        conn = None

        # Try create a connection, if any error crops up, print to output
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            if conn:
                # Close connection as a security measure
                conn.close()
    
    def append_dataframe_to_sql_table(self, df: DataFrame) -> None:
        """
        Write the contents of the dataframe to the sqlite database.
        """
        # Path to database
        database_path = f".\\{self.db_file}"
    
        # Setup connection to the db
        conn = sqlite3.connect(database_path)

        # Use the pandas to_sql function to append the data to the table
        df.to_sql(name=self.table_name, con=conn, if_exists="append", index=False)
