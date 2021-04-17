# Stocks_vs_SocialMedia

# NOTE: The project is under development 

## The main objective of this project is to determine the spike we may expect in stocks based on how trending it is.

# FRONTEND

1. We use REACT to build the front end and connect it to the backend model using API.

# BACKEND

1. We get real time data by DATA MINING using the praw library (specific to reddit) and create a data frame of multiple relevant pages from reddit

2. We get the current prices of all the trending stocks and how much spike (%) did we saw in the past STORING all the data in SQL

3. We ANALYZE the data to study the trend we may observe on based on the trends we gathered from the feed.

4. We perform a simple logistics regression to predict how much our stock will rise today based on how trending it is.
