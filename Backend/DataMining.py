"""DataMining.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/19c1YVbltQ-HHjTDbK-OsFvoVAkUHSFg5
"""


# Commented out IPython magic to ensure Python compatibility.
#########################################  DATA REQUESTS #############################################

# To provide current date and time in an format understandable by our API
from datetime import datetime
from datetime import timedelta
# Properly display html docs before we could work on it
from lxml import html
# Requests HTML data from websites and api
import requests
from requests import Request, Session

# Connecting with an API without any exceptions
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Clean the result from API's
import json
from bs4 import BeautifulSoup

##########################################  DATA MINING ##############################################

# To get posts from reddit
import praw

# To get the current stock prices
import yfinance as yf
from yahoo_fin.stock_info import get_data

# Connect to twitter API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy

from urllib.request import urlopen

# Library to set up email alerts
import smtplib

#######################################  DATA MANIPULATION ###########################################

import numpy as np
import pandas as pd
import csv
import re
import string
import os
import time

#######################################  DATA VISUALIZATION ###########################################

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pylab as plt
# %matplotlib inline
import seaborn as sns
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import mpld3
import plotly

########################################### DATA TRANSFER ############################################

from fastapi import FastAPI


#######################################################################################################

def Reddit_API(client_id, client_secret, username, password, subreddit, limit):
    """
    Receive the content of ``subreddit`` , establish credentials and retreive posts
    parse the data by iterating over the list.

    Parameters
    ----------
    client_id     : str
    client_secret : str
    username      : str
    password      : str
    subreddit     : str
    limit         : int

    Returns
    -------
    pd.DataFrame
    """
    #################### Establishing Credentials for Reddit ###################

    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = pd.DataFrame()
    params = {'limit': limit}
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {'User-Agent': 'data_analysis'}

    reddit = requests.post('https://www.reddit.com/api/v1/access_token',
                           auth=client_auth, data=data, headers=headers)

    ############################# Retrieving Data ##############################

    token = f"bearer {reddit.json()['access_token']}"
    headers = {**headers, **{'Authorization': token}}

    res_new = requests.get("https://oauth.reddit.com/r/" + subreddit + "/new",
                           headers=headers, params=params)
    res_top = requests.get("https://oauth.reddit.com/r/" + subreddit + "/top",
                           headers=headers, params=params)
    res_hot = requests.get("https://oauth.reddit.com/r/" + subreddit + "/hot",
                           headers=headers, params=params)
    res_rising = requests.get("https://oauth.reddit.com/r/" + subreddit + "/rising",
                              headers=headers, params=params)
    res_rec = requests.get("https://oauth.reddit.com/r/" + subreddit,
                           headers=headers, params=params)

    ############################### Parsing Data ###############################

    df = pd.DataFrame()
    posts = res_new.json()['data']['children']

    for post in posts:
        if post['data']['selftext']:
            df = df.append({'Title': post['data']['title'],
                            'Content': post['data']['selftext'],
                            'upvote_ratio': post['data']['upvote_ratio'],
                            'Upvotes': post['data']['ups'],
                            'score': post['data']['score'],
                            'type': post['data']['link_flair_css_class']
                            }, ignore_index=True)

    posts = res_top.json()['data']['children']
    for post in posts:
        if post['data']['selftext']:
            df = df.append({'Title': post['data']['title'],
                            'Content': post['data']['selftext'],
                            'upvote_ratio': post['data']['upvote_ratio'],
                            'Upvotes': post['data']['ups'],
                            'score': post['data']['score'],
                            'type': post['data']['link_flair_css_class']
                            }, ignore_index=True)

    posts = res_hot.json()['data']['children']
    for post in posts:
        if post['data']['selftext']:
            df = df.append({'Title': post['data']['title'],
                            'Content': post['data']['selftext'],
                            'upvote_ratio': post['data']['upvote_ratio'],
                            'Upvotes': post['data']['ups'],
                            'score': post['data']['score'],
                            'type': post['data']['link_flair_css_class']
                            }, ignore_index=True)

    posts = res_rising.json()['data']['children']
    for post in posts:
        if post['data']['selftext']:
            df = df.append({'Title': post['data']['title'],
                            'Content': post['data']['selftext'],
                            'upvote_ratio': post['data']['upvote_ratio'],
                            'Upvotes': post['data']['ups'],
                            'score': post['data']['score'],
                            'type': post['data']['link_flair_css_class']
                            }, ignore_index=True)

    posts = res_rec.json()['data']['children']
    for post in posts:
        if post['data']['selftext']:
            df = df.append({'Title': post['data']['title'],
                            'Content': post['data']['selftext'],
                            'upvote_ratio': post['data']['upvote_ratio'],
                            'Upvotes': post['data']['ups'],
                            'score': post['data']['score'],
                            'type': post['data']['link_flair_css_class']
                            }, ignore_index=True)

    ############################################################################

    return df


def getDataReddit(client_id, client_secret, username, password, user_agent, title, lt):
    """
    Receive the content of ``title`` (subreddit), establish credentials and retreive posts
    parse it using BeautifulSoup and return the DataFrame.
    Parameters
    ----------
    client_id     : str
    client_secret : str
    username      : str
    password      : str
    user_agent    : str
    title         : str
    lt            : int
    Returns
    -------
    pd.DataFrame
    """
    #################### Establishing Credentials for Reddit ###################

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    ############## Using Credentials established to retreive data ##############

    subreddit = reddit.subreddit(title)
    raw_data = subreddit.new(limit=lt)
    top_data = subreddit.top("week")

    ######################## Parsing the collected data ########################

    data = []

    for submission in top_data:
        data.append({'Title': submission.title,
                     'Content': BeautifulSoup(submission.selftext_html, "lxml").text,
                     'Upvotes': submission.ups, 'Downvotes': submission.downs})

    for submission in raw_data:
        data.append({'Title': submission.title,
                     'Content': BeautifulSoup(submission.selftext_html, "lxml").text,
                     'Upvotes': submission.ups, 'Downvotes': submission.downs})

    ############################################################################

    return pd.DataFrame(data)


def getTweets(consumer_key, consumer_secret, access_key, access_secret, hashtags, target_date, total_tweets,
                   attempts):
    """
    Receive the content of ``hashtags`` (tweets) by establishing credentials.
    Parse the data we want to use and return the DataFrame.
    Parameters
    ----------
    consumer_key    : str
    consumer_secret : str
    access_key      : str
    access_secret   : str
    hashtags        : str
    target_date     : str
    total_tweets    : int
    attempts        : int
    Returns
    -------
    pd.DataFrame
    """
    ################### Establishing Credentials for Twitter ###################

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    ############################# Retrieving Data ##############################

    # create an empty DataFrame to store tweets later
    db_tweets = pd.DataFrame(columns=['username', 'location', 'text', 'retweet_count'])
    count = 0

    # Collect all the tweets received in tweet_list for n attempts
    for i in range(0, attempts):
        tweets = tweepy.Cursor(api.search, q=hashtags, lang="en", since=target_date, tweet_mode='extended').items(
            total_tweets)
        tweet_list = [tweet for tweet in tweets]

    ######################## Parsing the collected data ########################

    for item in tweet_list:
        username, location, retweet_count = item.user.screen_name, item.user.location, item.retweet_count
        try:
            text = item.retweeted_status.full_text
        except AttributeError:
            text = item.full_text

        # Arrange and store the data collected for the tweet
        curr = [username, location, text, retweet_count]

        db_tweets.loc[len(db_tweets)] = curr
        count += 1

    ############################################################################

    # Good Night zzzzz
    time.sleep(900)
    return db_tweets


def clean(dataFrame):
    """
    Simply dropping duplicates from the dataframe.

    Parameters
    ----------
    dataFrame : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    dataFrame.drop_duplicates()
    return dataFrame



def stocks():
    """
    Receive the content of ``stock_dataset_url``, parse it using beautiful soup and return it as a DataFrame.
    Returns
    -------
    pd.DataFrame
    """
    ############################## Retrieving Data #############################

    stock_dataset_url = 'https://stockanalysis.com/stocks/'
    page = requests.get(stock_dataset_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    review = soup.find_all(class_='no-spacing')
    review_stocks = review[0].find_all('a')

    ############################### Parsing Data ###############################

    stock_list = []
    all_stocks = []
    for item in review_stocks:
        res = item.text.split('-')
        stock_list.append({'Ticker': res[0], 'Stock_Name': res[1]})
        all_stocks.append(res[1])

    ############################################################################

    return pd.DataFrame(stock_list)


# Get Top Gainers or Top Losers in the Stock Market Today
def Gainers_Or_Losers(x):
    """
    Receive the content of ``url``(Gainers if x == 1 else Losers), parse it as JSON and return the object.
    Parameters
    ----------
    x : int
    Returns
    -------
    pd.DataFrame
    """
    ############################# Retrieving Data ##############################

    url2 = ("https://financialmodelingprep.com/api/v3/losers?apikey=71a14544ca8435ff9b1d2ad551cf5b4e#0")
    url1 = ("https://financialmodelingprep.com/api/v3/stock/gainers?apikey=71a14544ca8435ff9b1d2ad551cf5b4e")
    response = urlopen(url1 if x == 1 else url2)
    data = response.read().decode("utf-8")

    ############################ Parsing Data(arr) #############################

    value = json.loads(data)
    try:
        arr = [item for item in value['mostGainerStock']]
    except:
        arr = [item for item in value]
    df = pd.DataFrame(arr)

    ############################################################################

    return df


def CoinBase_Api():
    """
    Receive the content of ``url``, parse it as JSON and return the data necessary as pd.DataFrame.
    Parameters
    ----------
    Returns
    -------
    pd.DataFrame
    """
    ############################# Retrieving Data ##############################

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'e5078d40-9c0f-45f5-8e1c-42c06a61b3c4',
    }

    session = Session()
    session.headers.update(headers)

    ############################# Parsing Data #################################

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        result = []
        for i in data['data']:
            result.append({'Name': i['name'],
                           'Symbol': i['symbol'],
                           'Price': i['quote']['USD']['price'],
                           'percent_change_1h': i['quote']['USD']['percent_change_1h'],
                           'percent_change_24h': i['quote']['USD']['percent_change_24h'],
                           'percent_change_7d': i['quote']['USD']['percent_change_7d'],
                           'percent_change_30d': i['quote']['USD']['percent_change_30d'],
                           'volume_24': i['quote']['USD']['volume_24h'],
                           'Trading_Volume': i['quote']['USD']['market_cap'],
                           'Circulating_Supply': i['circulating_supply']})
        return pd.DataFrame(result)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

    ############################################################################


def email_formatter(test_data):
    """
    Parse the DataFrame and convert it to a readable string
    Parameters
    ----------
    test_data : pd.DataFrame
    Returns
    -------
    str
    """
    ############################ Formatting the Data ###########################

    count = 1

    str_send = "List of Cryptos with growth over 500% today. \n\n\n"
    str_send += "{:<8} {:<35} {:<15} {:<15} {:<15}".format('No.', 'Name', 'Symbol', 'Price', 'Percent Change')
    str_send += "\n"

    for index, row in test_data.iterrows():
        price = '{:.7f}'.format(row['Price'])
        str_send += "{:<8} {:<35} {:<15} {:<15} {:<15}".format(count, row['Name'], row['Symbol'], price,
                                                               row['percent_change_24h'])
        str_send += "\n"
        count += 1

    ############################################################################

    return str_send


def Alerts(sender_email, sender_password, receiver_list):
    """
    Using the CoinBase_Api() email the top performing crytos and
    stocks to the receiver list provided.
    Parameters
    ----------
    sender_email    : str
    sender_password : str
    receiver_list   : list
    Returns
    -------
    E-mail
    """
    ############################ Collecting Data ###############################

    crypto_data = CoinBase_Api()
    stocks_gainers = Gainers_Or_Losers(1)
    # stocks_losers = Gainers_Or_Losers(0)

    # Get the cryptos where growth is over 500% and stocks where growth is over 10% in last 24h
    test_data = crypto_data.sort_values('percent_change_24h', ascending=False)
    test_data = test_data[test_data['percent_change_24h'] > 500]

    # Check whether there is any data to post or not
    to_post = len(test_data) > 0

    ################ E-mailing Results if Crypto growth > 500 ##################

    if to_post:
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(sender_email, sender_password)

        # Output Message
        TEXT = email_formatter(test_data)
        TEXT += "\n\n The Top Stock Gainers in the market today are : \n" + stocks_gainers.to_string() # + "\n\n The top Stock Losers in the market today are : \n" + stocks_losers.to_string()
        TEXT += "\n\n Have a good day \n Regards,\n Vrajesh"
        output_message = 'Subject: {}\n\n{}'.format("Crypto Alerts", TEXT)

        # sending the mail
        for receiver_email in receiver_list:
            s.sendmail(sender_email, receiver_email, output_message)

        # terminating the session
        s.quit()

    ############################################################################


# Establish Credentials
sender_email = 'cryptoalerts167@gmail.com'
sender_password = 'Kaboom001$$@'
receiver_list = ["harshghodkar@gmail.com"]
# Alerts(sender_email, sender_password, receiver_list)


def Common_words():
    """
    Get a list of common vocab words in english to eliminte common vocab
    similar to stock names from our list.
    Returns
    -------
    List
    """
    ############################# Retrieving Data ##############################

    page = requests.get('https://www.ef.com/ca/english-resources/english-vocabulary/top-3000-words/')
    word_html = BeautifulSoup(page.text, 'html.parser').find_all('p')[11]

    ############################# Parsing Data #################################

    counter = 0
    words = []
    for item in word_html:
        if counter % 2 == 0:
            words.append(item)
        counter += 1

    ############################################################################

    return words


def crypto_liquidity(crypto_data):
    """
    Get the current liquidity of all the stocks in the market. To actually analyze
    the crypto that has a steady demand in the market.
    Parameters
    ----------
    crypto_data : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    ############################# Retrieving Data ##############################

    page = requests.get('https://coinmarketcap.com/exchanges/digifinex/')
    soup = BeautifulSoup(page.text, 'lxml')
    review = soup.find_all(class_='cmc-table-row')

    ############################### Parsing Data ###############################

    data = []
    for item in review:
        # Using Regex for parsing
        regex = re.compile('[0-9]+')
        regex1 = re.compile('[A-Z][a-z]+')
        regex2 = re.compile('%[0-9]+')
        str_0 = item.text

        try:
            name = regex1.findall(str_0)[0]
        except:
            name = ""
        try:
            liquidity = regex2.findall(str_0)[0]
        except:
            liquidity = -1

        try:
            data.append({'Name': name, 'Liquidity': int(liquidity[1:])})
        except:
            data.append({'Name': name, 'Liquidity': liquidity})

    ########################### Merge Data Frames ##############################

    data = pd.DataFrame(data)
    data = data[data.Liquidity > 0]
    data = data.groupby('Name', group_keys=False).apply(lambda x: x.loc[x.Liquidity.idxmax()])
    data.reset_index(drop=True, inplace=True)
    data = pd.merge(left=crypto_data, right=data, how='left', left_on='Name', right_on='Name')
    data = data[data.Liquidity.notnull()]

    ############################################################################

    return data