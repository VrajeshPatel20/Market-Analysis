import pandas as pd
import DataMining as get_data
import Graphs
import AnalyzePosts as analyze
from datetime import datetime
from yahoo_fin.stock_info import get_data as get

###################################### Establish credentials ########################################

# Reddit
client_id, client_secret = 'jA6tGV9IbyEDxg', 'ku7t8VHg5vtp3JMGjuqJmE5ybQhBxA'
username, password = '-betrayer', 'NarutoUzamaki$$$'

# Twitter
consumer_key, consumer_secret = '02tFL0DX18rEZN43uV9iCWr6E', 'Bx3xDbD3a9fuP5Kv90ZGHD5amoJXAhF3l5sEElnp6H4esWDk1e'
access_key, access_secret = '1189932019243003904-85tElnlmswS7Of3dkiIzdImn2J4xiA', '6xt9bsQxlxyBUnR2p71mYYbZ42nDJK7TWCQPeAtsIL5zj'

################################## Get Posts and Tweets for stocks ##################################

# Retreive posts from reddit for stocks
reddit_posts = pd.DataFrame()
subreddits_stocks = ["wallstreetbets", "stocks", "investing", "securityanalysis"]
for subreddit in subreddits_stocks:
    new_data = get_data.Reddit_API(client_id, client_secret, username, password, subreddit, 10000)
    reddit_posts = reddit_posts.append(new_data)

# Retreive tweets from twitter
df_tweets = get_data.getTweets(consumer_key, consumer_secret, access_key, access_secret,
                               hashtags="#stocks OR #StockToBuy OR #trading OR #stockmarket OR #investing",
                               target_date='2021-04-30', total_tweets=2500, attempts=1)

######################################### Retreive Stocks Info #######################################

stocks = get_data.stocks()
common_words = get_data.Common_words()
top_gainers_today = get_data.Gainers_Or_Losers(1)
top_gainers_today.rename(columns={'ticker': 'Ticker'}, inplace=True)

################################### Analyze Reddit Posts and Tweets ###################################

Analysis_reddit = analyze.Analyze_Reddit_Posts(stocks, reddit_posts, common_words)
Analysis_tweets = analyze.Analyze_tweets(stocks,df_tweets, common_words)
Analysis_tweets = Analysis_tweets.sort_values('Number_Of_Occurences', ascending=False)
index_names = Analysis_tweets[ (Analysis_tweets['Number_Of_Occurences'] >= 10)].index
Analysis_tweets.drop(index_names, inplace = True)

###################################### Data Visualization ############################################

# Result of Reddit
Graphs.CombinedAnalysis_Stocks(Analysis_reddit, 20, 365)
Graphs.Stocks_candlePlots(Analysis_reddit, 10, 365)

# Result of Twitter
Graphs.CombinedAnalysis_Stocks(df_tweets, 20, 365)
Graphs.Stocks_candlePlots(df_tweets, 20, 365)

# Result of Market Performance
Graphs.CombinedAnalysis_Stocks(top_gainers_today, 20, 365)
Graphs.Stocks_candlePlots(top_gainers_today, 20, 365)

# 3D projection of relation between Occurences / Upvotes vs Price
# Analysis_reddit['Price'] = get(Analysis_reddit['Ticker'], datetime.now(), datetime.now())['close']
# Graphs.Analyze_Stocks_Posts(Analysis_reddit, 'Price', 'Total_Upvotes', 'Number_Of_Occurences')

# 3D projection of relation between Occurences / Retweets vs Price
Graphs.Analyze_Stocks_Posts(Analysis_tweets, 'Price', 'Total_Retweets', 'Number_Of_Occurences')

################################## Get Posts and Tweets for cryptos ##################################

# Retreive posts from reddit for crypto
reddit_crypto = pd.DataFrame()
subreddits_crypto = ["Bitcoinmarkets", "Ethfinance", "CryptoMarkets", "CryptoCurrencyTrading", "ethtrader",
                     "Cryptocurrency", "Crypto_Currency_News"]
for subreddit in subreddits_crypto:
    new_data = get_data.Reddit_API(client_id, client_secret, username, password, subreddit, 10000)
    reddit_crypto = reddit_crypto.append(new_data)
df_tweets_crypto = get_data.getTweets(consumer_key, consumer_secret, access_key, access_secret, hashtags="#Dogecoin OR #DogecoinToTheMoon OR #Dogearmy OR #doge", target_date='2021-04-30', total_tweets = 2500, attempts = 1)

######################################### Get Crypto rates ############################################

crypto_data = get_data.CoinBase_Api()
crypto_data = crypto_data[crypto_data.Circulating_Supply > 0]
crypto_data = crypto_data[crypto_data.volume_24 > 200000]
liquidable = get_data.crypto_liquidity(crypto_data)

################################# Analyze Reddit Posts and Tweets #####################################

RedditCrypto_Analysis = analyze.Analyze_Reddit_Crypto(crypto_data, reddit_crypto, common_words)
RedditCrypto_Analysis = RedditCrypto_Analysis.sort_values('Number_Of_Occurences', ascending=False)
RedditCrypto_Analysis = pd.merge(left=crypto_data, right=RedditCrypto_Analysis, how='left', left_on='Name',
                                 right_on='Name')

tweets_crypto = analyze.Analyze_Tweets_Crypto(crypto_data, df_tweets_crypto, common_words)
tweets_crypto = pd.merge(left=crypto_data, right=tweets_crypto, how='left', left_on='Name', right_on='Name')

###################################### Plot Graphs for Crpyto Analysis ################################

Graphs.Popular_Crypto(crypto_data=crypto_data, amt=20)
Graphs.Growing_Crypto(crypto_data=crypto_data, amt=20, period=24)

# Best Crypto's available with highest growth rate in last 24 hours
Graphs.Growing_Crypto_Investable(liquidable, 20, 24)

# Best Crypto's available with highest growth rate in last 7 days
Graphs.Growing_Crypto_Investable(liquidable, 20, 7)

# Analyze General Crypto Data
Graphs.Analyze_Crypto_Data(liquidable, 7)

# Analyze Crypto's based on Reddit Posts
Graphs.Analyze_Crypto_Posts(RedditCrypto_Analysis, 'Price', 'Total_Upvotes', 'Number_Of_Occurences')

# Analyze Crypto's based on Tweets
Graphs.Analyze_Crypto_Posts(tweets_crypto, 'Price', 'Total_Retweets', 'Number_Of_Occurences')

#######################################################################################################


###### EXTRA CODE ######

# To Use the praw library Uncomment the code below
# df = getDataReddit(client_id, client_secret, username, password, user_agent, 'stocks', 100)
# df = clean(df)
# reddit_posts = reddit_posts.append(df)

# Get Data from Tweets




