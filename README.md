# Axel

This project is a simple data pipeline which uses the Twitter API to extract daily tweet data (intended for tweets about stocks), then processes these tweets by adding sentiment score to them, using the VADER sentiment analysis model and finally uploads the tweets with their sentiment scores to a DropBox folder.
  
The project is named 'Axel' after the character Bobby Axelrod in the show 'Billions'... It was intented for stock value sentiment on Twitter... it made sense at the time...
  
The pipeline is run by the command `python src/orchestrator/orchestrator.py`.
  
## Setup

### Python Requirements
* The project uses Python version 3.8.10 - I strongly recommend using a virtual environment for the project, `python -m venv .<your_env_name>`
* To install the packages I used for dev run `pip install -r requirements.txt`
* To install the utility packages in the project, `cd` into the `src` directory and run `pip install -e .` - this will install the twitter and dropbox utils packages to your Python `site-packages`, hence my recommendation to use a virtual environment

### Credentials and Config
You will need to create a directory called `uncommitted` in the `src` directory - this will store config and credentials:
  
The file `.src/uncommitted/config.ini` file should have the following:
```
[TWEETS]
last_tweet_id = 0

[QUERIES]
query_dict_path = ./src/uncommitted/query_dict.json

[OUTPUT]
dropbox_write_path = /analyzed_tweets # Or whatever path you want
```
  
The file `./uncommitted/credentials.ini` should contain your tokens for the Twitter and DropBox APIs:
```
[TwitterAPI]
api_key = XXX
api_secret_key = XXX
bearer_api = XXX
access_token = XXX
access_token_secret = XXX

[DROPBOX]
app_key = XXX
app_secret = XXX
token = XXX
```
I found the following sources useful for the API setup:
  
* [Article on Twitter API](https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1)
* [DropBox Python SDK](https://www.dropbox.com/developers/documentation/python)
  
Finally you need to specify your twitter queries in a file `./src/uncommitted/query_dict.json`:
```
{
    "Standard Bank": { # Company Name
        "query": "$JSESBK", # Twitter query to use
        "geocode": "-28.8166236,24.991639,1000km" # Geocode for the query
    },
    "ABSA Bank": {
        "query": "$JSEABG",
        "geocode": "-28.8166236,24.991639,1000km"
    }
}
```

## Notes
While I do give the example of using it for sentiments on stocks, technically you could use the code to query any kind of tweet and measure it's sentiment.
  
This is a simple project that I used for learning purposes, but I hope you find some value in it.
If you have any comments or feedback please open up a PR, I'd appreciate it 😎.