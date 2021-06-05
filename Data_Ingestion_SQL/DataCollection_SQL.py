#########################################  DATA REQUESTS #############################################

# To provide current date and time in an format understandable by our API
from datetime import datetime

##########################################  DATA MINING ##############################################

import DataMining as get_data
from yahoo_fin.stock_info import get_data as get_val

#######################################  DATA MANIPULATION ###########################################

import pandas as pd
import AnalyzePosts as analyze
import sqlite3

############################ Establish credentials #############################

# Reddit
client_id, client_secret = 'jA6tGV9IbyEDxg', 'ku7t8VHg5vtp3JMGjuqJmE5ybQhBxA'
username, password = '-betrayer', 'NarutoUzamaki$$$'

# Twitter 
consumer_key, consumer_secret = 'Eoa8hFsMycFYsFyiOEeOW3mpb', 'JHCvRJO8EPe8IDq3wZ9Pcaw6RekSxNtue7KVGpXCz7ZZLSFAty'
access_key, access_secret = '1189932019243003904-85tElnlmswS7Of3dkiIzdImn2J4xiA', '6xt9bsQxlxyBUnR2p71mYYbZ42nDJK7TWCQPeAtsIL5zj'

######################## Get Posts and Tweets for stocks #######################

# Retreive posts from reddit for stocks
reddit_posts = pd.DataFrame()
subreddits_stocks = ["wallstreetbets", "stocks", "investing", "securityanalysis", "StockMarket"]
for subreddit in subreddits_stocks:
    new_data = get_data.Reddit_API(client_id, client_secret, username, password, subreddit, 10000)
    reddit_posts = reddit_posts.append(new_data)

# Retreive tweets from twitter 
df_tweets = get_data.getTweets(consumer_key, consumer_secret, access_key, access_secret, hashtags="#stocks OR #StockToBuy OR #trading OR #stockmarket OR #investing", target_date='2021-04-30', total_tweets = 2500, attempts = 1)

################################################################################

stocks = get_data.stocks()
common_words = get_data.Common_words()
top_gainers_today = get_data.Gainers_Or_Losers(1)
top_gainers_today.rename(columns={'ticker': 'Ticker'}, inplace=True)

################################################################################

Analysis_reddit = analyze.Analyze_Reddit_Posts(stocks, reddit_posts, common_words)

Analysis_tweets = analyze.Analyze_tweets(stocks,df_tweets, common_words)
Analysis_tweets = Analysis_tweets.sort_values('Number_Of_Occurences', ascending=False)
index_names = Analysis_tweets[(Analysis_tweets['Number_Of_Occurences'] >= 10)].index
Analysis_tweets.drop(index_names, inplace = True)

######################## Get Posts and Tweets for cryptos ######################

# Retreive posts from reddit for crypto
reddit_crypto = pd.DataFrame()
subreddits_crypto = ["Bitcoinmarkets", "Ethfinance", "CryptoMarkets", "CryptoCurrencyTrading", "ethtrader",
                     "Cryptocurrency", "Crypto_Currency_News", "dogecoin", "Bitcoin", "wallstreetbets"]
for subreddit in subreddits_crypto:
    new_data = get_data.Reddit_API(client_id, client_secret, username, password, subreddit, 10000)
    reddit_crypto = reddit_crypto.append(new_data)

df_tweets_crypto = get_data.getTweets(consumer_key, consumer_secret, access_key, access_secret, hashtags="#crypto OR #cryptocurrency OR #blockchain OR #bitcoin OR #ethereum", target_date='2021-05-2', total_tweets = 2500, attempts = 1)

############################## Get Crypto rates ################################

crypto_data = get_data.CoinBase_Api()
crypto_data = crypto_data[crypto_data.Circulating_Supply > 0]
crypto_data = crypto_data[crypto_data.volume_24 > 200000]
liquidable = get_data.crypto_liquidity(crypto_data)

####################### Analyze Reddit Posts and Tweets ########################

RedditCrypto_Analysis = analyze.Analyze_Reddit_Crypto(crypto_data, reddit_crypto, common_words)
RedditCrypto_Analysis = RedditCrypto_Analysis.sort_values('Number_Of_Occurences', ascending=False)
RedditCrypto_Analysis = pd.merge(left=crypto_data, right=RedditCrypto_Analysis, how='left', left_on='Name', right_on='Name')

tweets_crypto = analyze.Analyze_Tweets_Crypto(crypto_data, df_tweets_crypto, common_words)
tweets_crypto = pd.merge(left=crypto_data, right=tweets_crypto, how='left', left_on='Name', right_on='Name')

################################################################################

# Get the test data we require and the crypto must be trending 
test_reddit = RedditCrypto_Analysis[['Name', 'Price', 'Total_Upvotes','Positive_Upvotes', 'Negative_Upvotes', 'Neutral_Upvotes', 'Number_Of_Occurences', 'percent_change_24h','percent_change_7d']]
test_reddit = test_reddit[test_reddit['Number_Of_Occurences']>10]

test_twitter = tweets_crypto[['Name', 'Price', 'Total_Retweets', 'Number_Of_Occurences', 'percent_change_24h','percent_change_7d','Positive_Retweets', 'Negative_Retweets','Neutral_Retweets']]
test_twitter = test_twitter[test_twitter['Number_Of_Occurences']>10]

################################################################################

path_reddit = 'reddit.db'
path_twitter = 'twitter.db'

################################################################################

def create_connection(path, test_data):
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect(path)
        curr = conn.cursor()
        # curr.execute("""DROP TABLE IF EXISTS DATA;""")
        # curr.execute("""CREATE TABLE DATA (
        #               Name VARCHAR(20) NOT NULL, 
        #               Price DECIMAL, 
        #               Total_Upvotes INTEGER NOT NULL, 
        #               Positive_Upvotes INTEGER,
        #               Negative_Upvotes INTEGER, 
        #               Neutral_Upvotes INTEGER, 
        #               Number_Of_Occurences INTEGER,
        #               percent_change_24h DECIMAL, 
        #               percent_change_7d DECIMAL
        #               );""")
        # return pd.read_sql('select * from DATA', conn)
        test_data.columns = get_column_names_from_db_table(curr, 'DATA')
        
        test_data.to_sql(name='DATA', con=conn, if_exists='append', index=False)
        # conn.commit()
    except:
        print("ERROR")
    finally:
        if conn:
            conn.close()

def get_column_names_from_db_table(sql_cursor, table_name):
    """
    Scrape the column names from a database table to a list
    :param sql_cursor: sqlite cursor
    :param table_name: table name to get the column names from
    :return: a list with table column names
    """

    table_column_names = 'PRAGMA table_info(' + table_name + ');'
    sql_cursor.execute(table_column_names)
    table_column_names = sql_cursor.fetchall()

    column_names = list()

    for name in table_column_names:
        column_names.append(name[1])

    return column_names

#######################################################################

create_connection(path_reddit, test_reddit)
create_connection(path_twitter, test_twitter)